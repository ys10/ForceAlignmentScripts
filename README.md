# ForcedAlignmentScripts
A set of python scripts to process intermediate or final result files of *kaldi* forced alignment.

## Project Structure
* Scripts:
    - Some scripts named with a "create" prefix  for kaldi data prepare, such as *create_wav_scp.py*, *create_text.py*.
    - Some scripts for post processing merged alignment files, such as *trans_phone_ID_2_name.py*.
    - Some python scripts named with a "slice" prefix for slice final alignment file into separated sentence files.
* Directories:
    - resources: a directory to store some input files for ForcedAlignment program.
    - results: a directory to store some output files from ForcedAlignment program.
    - labs: a directory to store the seperated sentence alignment files sliced from merged alignment file.

## Steps for Forced Alignment
### Kaldi Download & install
Firstly, you need to download and install Kaldi successfully.Please checkout from kaldi repository on github, and fellow the guide of *README.md* in the repository.

reference:
[kaldi-asr](http://www.kaldi-asr.org/)

### Kaldi Forced Alignment
Secondly, you need to  prepare an environment for kaldi forced alignment, and start alignment process.

reference( just use first 5 steps shown at this page):
[kaldi-forcedalignment](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-forcedalignment.html)

#### Prepare directories
Create some directories to house your training data and models.

reference:
[Prepare directories](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training.html)

#### Create files for *data/train*
The files in *data/train* contain information regarding the specifics of the audio files, transcripts, and speakers. Specifically, it will contain the following files:
* **text**: The text file is essentially the utterance-by-utterance transcript of the corpus. You could create this file by run *create_text.py*.
* **segments**: The segments file contains the start and end time for each utterance in an audio file. You could create this file by run *create_segments.py*.
* **wav.scp**: The wav.scp file contains the location for each of the audio files.You could create this file by run *create_wav_scp.py*.
* **utt2spk**: The utt2spk file contains the mapping of each utterance to its corresponding speaker. You could create this file by run *create_utt2spk.py*.
* **spk2utt**: The spk2utt is a file that contains the speaker to utterance mapping.

reference:
[Create files for *data/train*](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training2.html)

#### Create files for *data/local/lang*
*data/local/lang* is the directory that contains language data specific to the your own corpus. For example, the lexicon only contains words and their pronunciations that are present in the corpus. This directory will contain the following:
* **lexicon.txt**: In *resource/* directory.
* **nonsilence_phones.txt**: As the name indicates, this file contains a list of all the phones that are not silence.
* **optional_silence.txt**: This file will simply contain a 'SIL' model.
* **silence_phones.txt**: This file will contain a 'SIL' (silence) and 'oov' (out of vocabulary) model.
* **extra_questions.txt(optional)**: A Kaldi script will generate a basic *extra_questions.txt* file for you, but in *data/lang/phones*. This file "asks questions" about a phone's contextual information by dividing the phones into two different sets. 

reference:
[Create files for *data/local/lang*](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training3.html)

#### Create files for *data/lang*
Now that we have all the files in *data/local/lang*, we need to generate all of the files in *data/lang*.

reference:
[Create files for *data/lang*](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training4.html)

#### Set the parallelization wrapper
Use **vim** to edit *cmd.sh* file

reference:
[Set the parallelization wrapper](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training5.html)

#### Create mfcc.conf file in conf folder
*mfcc.conf* contains the parameters for MFCC feature extraction. Use **vim** to edit it.

reference:
[Create mfcc.conf file in conf folder](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training6.html)

#### Extract MFCC features
Now we need to extract the MFCC acoustic features and compute the cepstral mean and variance normalization (CMVN) stats. This step may take you about 8 minutes(it depends on the sacle of your wave data).

**Notes**: The --nj option is for the number of jobs to be sent out, it's suggested been set equal to the number of speakers.

reference:
[Extract MFCC features](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training7.html)

#### Monophone training and alignment
Train & align monophone.

reference:
[Monophone training and alignment](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training8.html)

#### Triphone training and alignment
TODO

reference:
[Triphone training and alignment](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-training9.html)

#### Obtain CTM output from alignment files
**CTM** stands for time-marked conversation file and contains a time-aligned phoneme transcription of the utterances. You could obtain this file as fellows.

reference the 4th step shown at this page:
[kaldi-forcedalignment](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-forcedalignment.html)

#### Concatenate CTM files
reference the 5th step shown at this page:
[kaldi-forcedalignment](https://www.eleanorchodroff.com/tutorial/kaldi/kaldi-forcedalignment.html)

### Post Processing
Before visualize the alignment result, there are still some post processes to do.

#### Transform phone ID to phone name
Use *trans_phone_ID_2_name.py* to replace phone ID with phone name in the *merged_alignment.txt*. Before this process, you need to move *merged_alignment.txt* & *phones.txt* which produced by previous step to proper path corresponding to *trans_phone_ID_2_name.py*.The output file will be named with *final_align.txt*.

#### Slice alignment into seperated sentence file
Use *slice_merged_ali_2_labs.py* to slice *final_align.txt* produced by previous step into sentence file.

## Show alignment results
You can check the alignment results using [wavesurfer](https://sourceforge.net/projects/wavesurfer/).

## Transform alignment format(Optional)
In case of alignment format difference between different TTS Systems, a script should be applied to transform the format.

Use *trans_ali_format.py* to do this step. It depends on alignment format of your system, so this step is **optinal**.
