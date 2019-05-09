from data import *
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
import time
import numpy as np
import pickle


def build_extra_decoding_arguments(train_sents):
    """
    Receives: all sentences from training set
    Returns: all extra arguments which your decoding procedures requires
    """

    extra_decoding_arguments = {}
    ### YOUR CODE HERE
    ### END YOUR CODE

    return extra_decoding_arguments


def extract_features_base(curr_word, next_word, prev_word, prevprev_word, prev_tag, prevprev_tag):
    """
        Receives: a word's local information
        Returns: The word's features.
    """
    features = {}
    features['word'] = curr_word
    ### YOUR CODE HERE
    features['prev_tag'] = prev_tag
    features['prevprev_tag'] = prevprev_tag
    features['prev_tag_bigram'] = prev_tag + ' ' + prevprev_tag
    features['prev_word'] = prev_word
    features['prevprev_word'] = prevprev_word
    features['next_word'] = next_word
    # features['prev_word-tag'] = (prev_word, prev_tag)
    # features['prevprev_word-tag'] = (prevprev_word, prevprev_tag)
    features['initCap'] = 1 if re.match(r"^[A-Z]", curr_word) else 0
    features['hasNumeric'] = 1 if re.search(r"\d", curr_word) else 0
    features['hasDash'] = 1 if re.search(r"-", curr_word) else 0
    features['allCaps'] = 1 if re.search(r"^[A-Z]+$", curr_word) else 0
    #### suffixes + prefixes
    if len(curr_word) > 5:
        for i in xrange(4):
            features['prefix' + str(i + 1)] = curr_word[:i + 1]
            features['suffix' + str(i + 1)] = curr_word[- (i + 1):]
    ### END YOUR CODE
    return features

def extract_features(sentence, i):
    curr_word = sentence[i][0]
    prev_token = sentence[i - 1] if i > 0 else ('<st>', '*')
    prevprev_token = sentence[i - 2] if i > 1 else ('<st>', '*')
    next_token = sentence[i + 1] if i < (len(sentence) - 1) else ('</s>', 'STOP')
    return extract_features_base(curr_word, next_token[0], prev_token[0], prevprev_token[0], prev_token[1], prevprev_token[1])

def vectorize_features(vec, features):
    """
        Receives: feature dictionary
        Returns: feature vector

        Note: use this function only if you chose to use the sklearn solver!
        This function prepares the feature vector for the sklearn solver,
        use it for tags prediction.
    """
    example = [features]
    return vec.transform(example)

def create_examples(sents, tag_to_idx_dict):
    examples = []
    labels = []
    num_of_sents = 0
    for sent in sents:
        num_of_sents += 1
        for i in xrange(len(sent)):
            features = extract_features(sent, i)
            examples.append(features)
            labels.append(tag_to_idx_dict[sent[i][1]])

    return examples, labels


def memm_greedy(sent, logreg, vec, index_to_tag_dict, extra_decoding_arguments):
    """
        Receives: a sentence to tag and the parameters learned by memm
        Returns: predicted tags for the sentence
    """
    predicted_tags = [""] * (len(sent))
    """
    logreg - class sklearn.linear_model.LinearRegression
    vec - class sklearn.feature_extraction.DictVectorizer
    index_to_tag_dict - class dictionary from number to
    extra_decoding_arguments
    """
    ### YOUR CODE HERE
    for j, word in enumerate(sent):
        features = extract_features(sent, j)
        word_vec = vec.transform(features)
        tag = logreg.predict(word_vec)
        prob = logreg.predict_proba(word_vec)
        predicted_tags[j] = index_to_tag_dict[tag[0]]  # tag is ndarray
        
    ### END YOUR CODE
    return predicted_tags

def memm_viterbi(sent, logreg, vec, index_to_tag_dict, extra_decoding_arguments):
    """
        Receives: a sentence to tag and the parameters learned by memm
        Returns: predicted tags for the sentence
    """
    predicted_tags = [""] * (len(sent))
    ### YOUR CODE HERE
    raise NotImplementedError
    ### END YOUR CODE
    return predicted_tags

def should_log(sentence_index):
    if sentence_index > 0 and sentence_index % 10 == 0:
        if sentence_index < 150 or sentence_index % 200 == 0:
            return True

    return False


def memm_eval(test_data, logreg, vec, index_to_tag_dict, extra_decoding_arguments):
    """
    Receives: test data set and the parameters learned by memm
    Returns an evaluation of the accuracy of Viterbi & greedy memm
    """
    acc_viterbi, acc_greedy = 0.0, 0.0
    eval_start_timer = time.time()

    correct_greedy_preds = 0
    correct_viterbi_preds = 0
    total_words_count = 0

    for i, sen in enumerate(test_data):
        ### YOUR CODE HERE
        ### Make sure to update Viterbi and greedy accuracy
        # sen_features = [extract_features(sen, i) for i in xrange(len(sen))]
        # sen_vec = vec.transform(sen_features)
        greedy_tags = memm_greedy(sen, logreg, vec, index_to_tag_dict, extra_decoding_arguments)
        ### END YOUR CODE

        if should_log(i):
            if acc_greedy == 0 and acc_viterbi == 0:
                raise NotImplementedError
            eval_end_timer = time.time()
            print str.format("Sentence index: {} greedy_acc: {}    Viterbi_acc:{} , elapsed: {} ", str(i), str(acc_greedy), str(acc_viterbi) , str (eval_end_timer - eval_start_timer))
            eval_start_timer = time.time()

    acc_greedy = float(correct_greedy_preds) / float(total_words_count)
    acc_viterbi = float(correct_viterbi_preds) / float(total_words_count)

    return str(acc_viterbi), str(acc_greedy)

def build_tag_to_idx_dict(train_sentences):
    curr_tag_index = 0
    tag_to_idx_dict = {}
    for train_sent in train_sentences:
        for token in train_sent:
            tag = token[1]
            if tag not in tag_to_idx_dict:
                tag_to_idx_dict[tag] = curr_tag_index
                curr_tag_index += 1

    tag_to_idx_dict['*'] = curr_tag_index
    return tag_to_idx_dict


if __name__ == "__main__":
    #### For faster debugging - saved all the non Q4 objects in pickle###
    if os.path.exists("C:\\Users\\eytanc\\Documents\\GitHub\\NLP_HW\\NLP_HW\\hw3\\pickles\\initial_objs1234.pkl"):
        full_flow_start = time.time()
        print "Opening initial_objs.pkl...."
        start = time.time()
        with open("C:\\Users\\eytanc\\Documents\\GitHub\\NLP_HW\\NLP_HW\\hw3\\pickles\\initial_objs.pkl", 'rb') as f:
            train_sents, dev_sents, vocab, extra_decoding_arguments, tag_to_idx_dict, index_to_tag_dict = pickle.load(f)
        end = time.time()
        print "Opening took %s" % (start - end)
        print "Opening data_objs.pkl...."
        start = time.time()
        with open("C:\\Users\\eytanc\\Documents\\GitHub\\NLP_HW\\NLP_HW\\hw3\\pickles\\data_objs.pkl", 'rb') as f:
            train_examples, train_labels, dev_examples, dev_labels, all_examples_vectorized, train_examples_vectorized, dev_examples_vectorized = pickle.load(f)
        end = time.time()
        print "Opening took %s" % (start - end)
        start = time.time()
        print "Opening model.pkl...."
        with open("C:\\Users\\eytanc\\Documents\\GitHub\\NLP_HW\\NLP_HW\\hw3\\pickles\\model.pkl", 'rb') as f:
            logreg, vec = pickle.load(f)
        end = time.time()
        print "Opening took %s" % (start - end)
    else:
        full_flow_start = time.time()
        train_sents = read_conll_pos_file("Penn_Treebank/train.gold.conll")
        dev_sents = read_conll_pos_file("Penn_Treebank/dev.gold.conll")
    
        vocab = compute_vocab_count(train_sents)
        train_sents = preprocess_sent(vocab, train_sents)
        extra_decoding_arguments = build_extra_decoding_arguments(train_sents)
        dev_sents = preprocess_sent(vocab, dev_sents)
        tag_to_idx_dict = build_tag_to_idx_dict(train_sents)
        index_to_tag_dict = invert_dict(tag_to_idx_dict)
    
        vec = DictVectorizer()
        print "Create train examples"
        train_examples, train_labels = create_examples(train_sents, tag_to_idx_dict)
    
    
        num_train_examples = len(train_examples)
        print "#example: " + str(num_train_examples)
        print "Done"
    
        print "Create dev examples"
        dev_examples, dev_labels = create_examples(dev_sents, tag_to_idx_dict)
        num_dev_examples = len(dev_examples)
        print "#example: " + str(num_dev_examples)
        print "Done"
    
        all_examples = train_examples
        all_examples.extend(dev_examples)
    
        print "Vectorize examples"
        all_examples_vectorized = vec.fit_transform(all_examples)
        train_examples_vectorized = all_examples_vectorized[:num_train_examples]
        dev_examples_vectorized = all_examples_vectorized[num_train_examples:]
        print "Done"
        end_make_vars = time.time()
        print "Making var took %s" % (full_flow_start - end_make_vars)
        logreg = linear_model.LogisticRegression(
            multi_class='multinomial', max_iter=128, solver='lbfgs', C=100000, verbose=1)
        print "Fitting..."
        start = time.time()
        logreg.fit(train_examples_vectorized, train_labels)
        end = time.time()
        print "End training, elapsed " + str(end - start) + " seconds"
        # End of log linear model training
    
        with open("C:\\Users\\eytanc\\Documents\\GitHub\\NLP_HW\\NLP_HW\\hw3\\pickles\\initial_objs.pkl", 'wb') as f:
            pickle.dump([train_sents, dev_sents,vocab,extra_decoding_arguments,tag_to_idx_dict,index_to_tag_dict], f, protocol=-1)
        with open("C:\\Users\\eytanc\\Documents\\GitHub\\NLP_HW\\NLP_HW\\hw3\\pickles\\data_objs.pkl", 'wb') as f:
            pickle.dump([train_examples,train_labels,dev_examples,dev_labels,all_examples_vectorized,train_examples_vectorized,dev_examples_vectorized], f, protocol=-1)
        with open("C:\\Users\\eytanc\\Documents\\GitHub\\NLP_HW\\NLP_HW\\hw3\\pickles\\model.pkl", 'wb') as f:
            pickle.dump([logreg, vec], f, protocol=-1)
    
    # Evaluation code - do not make any changes
    start = time.time()
    print "Start evaluation on dev set"

    acc_viterbi, acc_greedy = memm_eval(dev_sents, logreg, vec, index_to_tag_dict, extra_decoding_arguments)
    end = time.time()
    print "Dev: Accuracy greedy memm : " + acc_greedy
    print "Dev: Accuracy Viterbi memm : " + acc_viterbi

    print "Evaluation on dev set elapsed: " + str(end - start) + " seconds"
    if os.path.exists('Penn_Treebank/test.gold.conll'):
        test_sents = read_conll_pos_file("Penn_Treebank/test.gold.conll")
        test_sents = preprocess_sent(vocab, test_sents)
        start = time.time()
        print "Start evaluation on test set"
        acc_viterbi, acc_greedy = memm_eval(test_sents, logreg, vec, index_to_tag_dict, extra_decoding_arguments)
        end = time.time()

        print "Test: Accuracy greedy memm: " + acc_greedy
        print "Test:  Accuracy Viterbi memm: " + acc_viterbi

        print "Evaluation on test set elapsed: " + str(end - start) + " seconds"
        full_flow_end = time.time()
        print "The execution of the full flow elapsed: " + str(full_flow_end - full_flow_start) + " seconds"