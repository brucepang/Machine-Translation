# Machine Translation

### Train the IBM Model 1 on English corpus and foreign corpus
```
python model1.py train corpus.en corpus.es
```
t (tranlation) parameters will be saved to the /parameters directory

### Test the trained model on development dataset
```
python model1.py eval corpus.en corpus.es
```
Result will be written as the format of alignment to a local file

### Evaluate the written alignment with gold alignment
```
python eval alignments.py dev.key dev.out
```
Result score will be printed to the console.

### Train the IBM Model 2 on English corpus and foreign corpus
```
python model2.py train corpus.en corpus.es
```
t (tranlation) parameters will be saved to the /parameters directory

### Test the trained model on development dataset
```
python model2.py eval corpus.en corpus.es
```
Result will be written as the format of alignment to a local file

### Evaluate the written alignment with gold alignment
```
python eval alignments.py dev.key dev.out
```
Result score will be printed to the console.



### Grow the alignment
```
python grow.py
```
Grown alignment will be written into dev_grow.out

### Evaluate the written alignment with gold alignment
```
python eval alignments.py dev.key dev_grow.out
```
Result score will be printed to the console.

