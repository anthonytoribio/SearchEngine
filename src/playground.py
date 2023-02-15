from nltk.stem import SnowballStemmer
SNOWBALL = SnowballStemmer(language="english")

print(SNOWBALL.stem("i'm"))