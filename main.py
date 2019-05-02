import pandas, re, time

def ngram(text, n):
    df = pandas.DataFrame(columns=['Frequency'])
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text).split()
    if n>1: #only do concatenation if we need to consolidate the split
        text = [' '.join(text[i:i+n]) for i in range(len(text)-n)]
    text.sort()
    nWordList = list(set(text))
    nWordList.sort()
    print(len(nWordList), len(text))
    counter=0
    index=0
    for word in nWordList:
        count=0
        while index<len(text) and text[index]==word:
            count+=1
            index+=1
        df.loc[word]=count
        if counter%1000==0 and counter!=0:
            print(counter)
            # choose to save it in a csv file because it exceeds the total number of rows in Excel
            # in certain cases eg: 1.8 million rows for 2-grams whereas Excel only has 2^20 rows.
            df.to_csv(str(n) + '-gram outputs.csv', header=False if counter>1000 else True, mode='a')
            df.drop(df.index, inplace=True)
        counter+=1
    # write the remaining mod 1000 rows into file
    df.to_csv(str(n) + '-gram outputs.csv', header=False if counter>1000 else True, mode='a')
    del df

def main():
    jsonData = pandas.read_json('News_Category_Dataset_v2.json', lines=True)
    n = 2

    text = ' '.join(jsonData['short_description'].tolist() + jsonData['headline'].tolist())
    for i in range(1,n+1):
        ngram(text, i)

if __name__=='__main__':
    main()
