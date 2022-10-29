# Ada.py
Upload of the Statistical Methods for Machine Learning exam project on Adaboost development from scratch done in 2019.

## Requirements
This software requires **Python3**, available [here](https://www.python.org/).

## How to use it
Type in bash the following code:

```
python .\Adaboost.py T
```
\*It can be python3 based on the environment variable.

The parameter T indicates the number of decision stumps to be used. These are generated automatically in the code from the dataset.

One possible execution is as follows:

```
python .\Adaboost.py 200
```
## Results obtained

Results:

| Class Errors \ T    | 200                  | 400                  | 600                  | 800                  |
|---------------------|----------------------|----------------------|----------------------|----------------------|
| Class 1 Train Error | 0.09947089947089947  | 0.09753086419753086  | 0.09753086419753086  | 0.09611992945326278  |
| Class 1 Test Error  | 0.09947089947089947  | 0.09841269841269841  | 0.0992063492063492   | 0.09841269841269841  |
| Class 2 Train Error | 0.11190476190476191  | 0.11031746031746031  | 0.10864197530864197  | 0.10767195767195767  |
| Class 2 Test Error  | 0.11296296296296296  | 0.11481481481481481  | 0.11481481481481481  | 0.1164021164021164   |
| Class 3 Train Error | 0.10564373897707231  | 0.10220458553791888  | 0.10291005291005291  | 0.1019400352733686   |
| Class 3 Test Error  | 0.11587301587301588  | 0.11507936507936507  | 0.11587301587301588  | 0.1164021164021164   |
| Class 4 Train Error | 0.026102292768959437 | 0.024074074074074074 | 0.023192239858906526 | 0.022663139329805997 |
| Class 4 Test Error  | 0.02857142857142857  | 0.0291005291005291   | 0.028835978835978836 | 0.029365079365079365 |
| Class 5 Train Error | 0.06499118165784833  | 0.06031746031746032  | 0.059171075837742504 | 0.05793650793650794  |
| Class 5 Test Error  | 0.07116402116402117  | 0.06428571428571428  | 0.06375661375661376  | 0.06296296296296296  |
| Class 6 Train Error | 0.09876543209876543  | 0.09559082892416226  | 0.09329805996472663  | 0.09074074074074075  |
| Class 6 Test Error  | 0.11084656084656085  | 0.10185185185185185  | 0.10264550264550265  | 0.10238095238095238  |
| Class 7 Train Error | 0.02962962962962963  | 0.029012345679012345 | 0.02857142857142857  | 0.027777777777777776 |
| Class 7 Test Error  | 0.03333333333333333  | 0.03306878306878307  | 0.0328042328042328   | 0.0328042328042328   |
