import json
import numpy as np

def generate_json_output(data, filename):
    class NumpyFloatValuesEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (type(np.float32()), type(np.float64()))):
                return float(obj)
            return json.JSONEncoder.default(self, obj)
            
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, cls=NumpyFloatValuesEncoder, ensure_ascii=False)