import itertools
import json

from gensim.models.word2vec import LineSentence, Word2Vec

from comments.models import Comment


def get_dataset_sentences():
    sentences = []

    dataset = json.load(open('ensemble/dataset.json'))
    for text in dataset:
        sentences.append(text.split())
    return sentences


def get_sentences():
    #./manage.py shell -c="from ensemble.hate2vec import get_sentences; get_sentences()"
    sentences = get_dataset_sentences()

    comments = Comment.objects.all().values_list('text', flat=True)
    for text in comments:
        sentences.append(text.split())

    return sentences


def build_model(fname='ensemble/model.w2v'):
    #./manage.py shell -c="from ensemble.hate2vec import build_model; build_model()"
    sentences = get_sentences()
    model = Word2Vec(sentences, size=100, window=5, min_count=3, workers=4)
    model.save(fname)


def build_badvocab(fbadword='ensemble/badword_list.json', fbadvocab='ensemble/badvocab.json', fvocab='ensemble/vocab.json'):
    #./manage.py shell -c="from ensemble.hate2vec import build_badvocab; build_badvocab()"
    sentences = get_dataset_sentences()
    sentences = itertools.chain.from_iterable(sentences)
    vocab = set(sentences)

    badword_list = json.load(open(fbadword))
    badvocab = vocab.intersection(set(badword_list))
    with open(fbadvocab, 'w') as outfile:
        json.dump(list(badvocab), outfile)

    with open(fvocab, 'w') as outfile:
        json.dump(list(vocab), outfile)


def get_similarities(fname='ensemble/model.w2v', fbadvocab='ensemble/badvocab.json', fvocab='ensemble/vocab.json'):
    #./manage.py shell -c="from ensemble.hate2vec import get_similarities; get_similarities()"
    model = Word2Vec.load(fname)
    vocab = json.load(open(fvocab))
    badvocab = json.load(open(fbadvocab))
    badvocab = set(badvocab)
    vocab = list(set(vocab) - badvocab)
    new_badvocab = set(badvocab)

    for word in vocab:
        try:
            sims = model.wv.most_similar(positive=[word])
        except:
            continue
        words = set(w[0] for w in sims)
        inter = words.intersection(badvocab)
        if len(inter) > 0:
            new_badvocab.add(word)
    return set(new_badvocab)


def classifier():
    #./manage.py shell -c="from ensemble.hate2vec import classifier; classifier()"
    sentences = get_dataset_sentences()
    badvocab = get_similarities()

    for sentence in sentences:
        inter = set(sentence).intersection(badvocab)
        if len(inter) > 0:
            print(1)
        else:
            print(0)
