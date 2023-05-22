import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

class TOEICBert():
    """
    Model using pretrained Bert for answering toeic question, running for each example
    Bertmodel: we can choose bert large cased/bert large uncased, etc
    
    Model return the answer for the question based on the highest probability
    """

    def __init__(self, bertmodel):
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        # Initial tokenizer to tokenize the question later
        self.tokenizer = AutoTokenizer.from_pretrained(bertmodel)
        self.model = AutoModelForMaskedLM.from_pretrained(
            bertmodel).to(self.device)
        # We used pretrained BertForMaskedLM to fill in the blank, do not fine tuning so we set model to eval
        self.model.eval()

    def get_score(self, question_tensors, segment_tensors, masked_index, candidate):
        # Tokenize the answer candidate
        candidate_tokens = self.tokenizer.tokenize(candidate)
        # After tokenizing, we convert token to ids, (word to numerical)
        candidate_ids = self.tokenizer.convert_tokens_to_ids(candidate_tokens)
        predictions = self.model(question_tensors, segment_tensors)
        predictions_candidates = predictions[0,
                                             masked_index, candidate_ids].mean()
        return predictions_candidates.item()

    def predict(self, row):
        # Tokenizing questions, convert '___' to '_' so that we can MASK it
        question_tokens = self.tokenizer.tokenize(
            row['question'].replace('___', '_'))
        masked_index = question_tokens.index('_')
        # Assign [MASK] to blank that need to be completed
        question_tokens[masked_index] = '[MASK]'
        segment_ids = [0] * len(question_tokens)
        segment_tensors = torch.tensor([segment_ids]).to(self.device)
        question_ids = self.tokenizer.convert_tokens_to_ids(question_tokens)
        question_tensors = torch.tensor([question_ids]).to(self.device)
        candidates = row['options']
        # Return probabilities of answer choice [prob1, prob2, prob3, prob4]
        predict_tensor = torch.tensor([self.get_score(question_tensors, segment_tensors,
                                                      masked_index, candidate) for candidate in candidates])
        # Softmax the predict probability to return the index for maximum values
        predict_idx = torch.argmax(predict_tensor).item()
        return candidates[predict_idx]
