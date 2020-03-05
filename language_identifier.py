import os
import sys

import torch
import torchaudio
import pytorch_lightning as pl

# TODO: Find a better solution for importing model architecture
sys.path.append('/export/home/jovalk/lang-id-server/pytorch_models')

from .pytorch_models.models import XVectorModel


class LanguageIdentifier:
        
    TOP_RESULTS_COUNT = 5

    def __init__(self):
        cpu = torch.device('cpu')
        current_path = os.path.dirname(__file__)
        model_checkpoint = os.path.join(current_path, 'pytorch_models/checkpoint.ckpt')

        self.model = XVectorModel.load_from_checkpoint(model_checkpoint).to(cpu)
        self.model.eval()
        self.model.freeze()


    def identify_language(self, input_file_path: str):
        input_wav = torchaudio.load(input_file_path, normalization=1 << 31)[0]

        y_hat = self.model(self.model.wav_to_features(input_wav))

        softmax = torch.nn.Softmax(dim=1)
        probabilities = softmax(y_hat)

        probabilities_top = torch.topk(probabilities, self.TOP_RESULTS_COUNT)
        labels_top = torch.topk(y_hat, self.TOP_RESULTS_COUNT)

        probabilities_top_values = probabilities_top.values.squeeze(0).tolist()
        labels_top_values = labels_top.values.squeeze(0).tolist()
        labels_top_indices = labels_top.indices.squeeze(0).tolist()

        lang_names = [k for k in self.model.chunk_dataset_factory.label2id]

        result = []
        for idx, value in enumerate(labels_top_values):
            obj = {}
            obj['language'] = lang_names[labels_top_indices[idx]]
            obj['value'] = value
            obj['probability'] = probabilities_top_values[idx]

            result.append(obj)

        return result
