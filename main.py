import pandas, re, time

def ngram(df, text, n):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text).split()
    # print(len(text))
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
            df.to_csv(str(n) + '-gram outputs.csv', header=False if counter>1000 else True, mode='a')
            df.drop(df.index, inplace=True)
        counter+=1

def main():
    jsonData = pandas.read_json('News_Category_Dataset_v2.json', lines=True)
    df = pandas.DataFrame(columns=['Frequency'])
    n = 2

    text = ' '.join(jsonData['short_description'].tolist() + jsonData['headline'].tolist())
    for i in range(1,n+1):
        ngram(df, text, i)

if __name__=='__main__':
    main()