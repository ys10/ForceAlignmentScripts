#cd forced-alignment directory
script_dir=.
data_dir=/home/voicedata/xiaochang
kaldi_dir=../kaldi-master
corpus_name=mycorpus_en
python3 $script_dir/create_text.py -i $data_dir/utterance_en.txt  -o results/text
python3 $script_dir/create_wav_scp.py -i $data_dir/wave -o results/wav.scp
python3 $script_dir/create_segments.py -i $data_dir/wave -o results/segments
python3 $script_dir/create_utt2spk.py -i results/wav.scp -o results/utt2spk

:<<BLOCK
Prepare kaldi directories
BLOCK
cd $kaldi_dir/egs
mkdir $corpus_name
cd $corpus_name
ln -s ../wsj/s5/steps .
ln -s ../wsj/s5/utils .
ln -s ../../src .
cp ../wsj/s5/path.sh .
echo "export KALDI_ROOT='pwd'/../../.. to export KALDI_ROOT='pwd'/../.." > path.sh

mkdir exp
mkdir conf
mkdir data

cd data
mkdir train
mkdir lang
mkdir local

cd local
mkdir lang

#cd $corpus_name
cd ../..


:<<BLOCK
Create files for data/train
BLOCK
resource_dir=../../../ForceAlignmentScripts/results
train_dir=data/train
#text
cp $resource_dir/text $train_dir/
cut -d ' ' -f 2- text | sed 's/ /\n/g' | sort -u > words.txt
#segments
cp $resource_dir/segments $train_dir/
#wav.scp
cp $resource_dir/wav.scp $train_dir/
#utt2spk
cp $resource_dir/utt2spk $train_dir/
#create spk2utt
utils/fix_data_dir.sh $train_dir


:<<BLOCK
....Create files for data/local/lang
BLOCK
lang_dir=data/local/lang
#lexicon.txt
cp $resource_dir/lexicon.txt $lang_dir/
python3 filter_dict.py
#nonsilence_phones.txt
cut -d ' ' -f 2- $lang_dir/lexicon.txt | sed 's/ /\n/g' | sort -u > $lang_dir/nonsilence_phones.txt
#silence_phones.txt
echo "sil" > $lang_dir/silence_phones.txt
echo "oov" >> $lang_dir/silence_phones.txt
#optinal_phones.txt
echo "sil" > $lang_dir/optional_silence.txt
#extra_questions.txt
echo "" > $lang_dir/extra_questions.txt

:<<BLOCK
....Create files for data/lang
....where the underlying argument structure is:
....utils/prepare_lang.sh <dict-src-dir> <oov-dict-entry> <tmp-dir> <lang-dir>
BLOCK
utils/prepare_lang.sh $lang_dir 'oov' data/local/ data/lang


:<<BLOCK
Set the parallelization wrapper
BLOCK
echo "train_cmd=\"run.pl\"" > cmd.sh
echo "decode_cmd=\"run.pl --mem 2G\"" >> cmd.sh
. ./cmd.sh


:<<BLOCK
....Extract MFCC features
BLOCK

#Create mfcc.conf file in conf folder
echo "--use-energy=false" > conf/mfcc.conf
echo "--sample-frequency=44100" >> conf/mfcc.conf
#Extract MFCC features
mfccdir=mfcc
x=data/train
steps/make_mfcc.sh --cmd "$train_cmd" --nj 1 $x exp/make_mfcc/$x $mfccdir
steps/compute_cmvn_stats.sh $x exp/make_mfcc/$x $mfccdir

:<<BLOCK
....Train & align monophones
BLOCK
#Train monophones
steps/train_mono.sh --boost-silence 1.25 --nj 1 --cmd "$train_cmd" data/train data/lang exp/train_mono
#Align monophones
steps/align_si.sh --boost-silence 1.25 --nj 1 --cmd "$train_cmd" data/train data/lang exp/train_mono exp/ali_mono


:<<BLOCK
....Train & align triphones
BLOCK
#Train delta-based triphones
steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" 2000 10000 data/train data/lang exp/ali exp/tri1
#Align delta-based triphones
steps/align_si.sh --nj 1 --cmd "$train_cmd" data/train data/lang exp/tri1 exp/tri1_ali


#Train delta + delta-delta triphones
steps/train_deltas.sh --cmd "$train_cmd" 2500 15000 data/train data/lang exp/tri1_ali exp/tri2a
#Align delta + delta-delta triphones
steps/align_si.sh --nj 1 --cmd "$train_cmd" --use-graphs true data/train data/lang exp/tri2a exp/tri2a_ali


#Train LDA-MLLT triphones
steps/train_lda_mllt.sh --cmd "$train_cmd" 3500 20000 data/train data/lang exp/tri2a_ali exp/tri3a
#Align LDA-MLLT triphones
steps/align_fmllr.sh --nj 1 --cmd "$train_cmd" data/train data/lang exp/tri3a exp/tri3a_ali


#Train SAT triphones
steps/train_sat.sh --cmd "$train_cmd" 4200 40000 data/train data/lang exp/tri3a_ali exp/tri4a
#Align SAT triphones
steps/align_fmllr.sh --cmd "$train_cmd" data/train data/lang exp/tri4a exp/tri4a_ali


:<<BLOCK
....Obtain CTM output from alignment files
BLOCK
for i in exp/tri4a_alignme/ali.*.gz;
do src/bin/ali-to-phones --ctm-output exp/tri4a/final.mdl ark:"gunzip -c $i|" -> ${i%.gz}.ctm;
done;


:<<BLOCK
....Concatenate CTM files
BLOCK
cat *.ctm > exp/tri4a_ali/merged_alignment.txt


:<<BLOCK
....Post process
BLOCK
#move merged_alignment.txt & phones.txt
cp exp/tri4a_ali/merged_alignment.txt ../../../script_dir/results/
cp exp/tri4a_ali/phones.txt ../../../script_dir/results/

#cd forced-alignment project directory
cd ../../../script_dir

#Transform phone ID to phone name
python3 trans_phone_ID_2_name.py -p results/phones.txt -i results/merged_alignment.txt -o results/final_align.txt
#Slice alignment into separated sentence file
python3 slice_merged_ali_2_labs.py -i results/mono_final_align.txt -o labs/ali_tri4 -p tri4_
