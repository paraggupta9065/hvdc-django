# Project Setup with Django Rest Framework

## Prerequisites:
- Python installed on your system (preferably Python 3.6 or higher)
- pip (Python package installer) installed

## Steps:

### 1. Create a Virtual Environment:
It's recommended to work within a virtual environment to isolate your project dependencies. Use the following command:

python -m venv my-env

### 2. Activate the Virtual Environment:
On Windows: my-env\Scripts\activate

On Unix or MacOS: source my-env/bin/activate

### 3. Install Dependencies:
Run the following command to install the dependencies listed in the `requirements.txt` file:

pip install -r requirements.txt


## Usage Of Code Template

### Mixins for Models, API Views, and Viewsets:

To use these mixins, follow these steps:

1. Import the mixins into your views or viewsets.
2. Inherit from the appropriate mixin(s) along with the necessary DRF viewsets.
3. Define the queryset and serializer class as usual.

### Example:

Here's an example of how to use the mixins in a viewset:

```python
from rest_framework.viewsets import ModelViewSet
from .models import YourModel
from .mixins import ModelCRUDViewSetMixin
from .serializers import YourModelSerializer

class YourModelViewSet(ModelCRUDViewSetMixin, ModelViewSet):
    """
    A viewset that provides CRUD actions for YourModel.
    """
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer


