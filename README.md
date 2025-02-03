# Generative Models and Recommender Systems for AI-driven Fashion
- This repository contains my work done as part of my **undergraduate thesis** titled **"Generative Models and Recommender Systems for AI-driven Fashion"** at OUTR.

## Abstract

Artificial Intelligence has profoundly transformed the fashion industry, reshaping design, production, and consumer engagement. In particular, AI-driven techniques have revolutionized fashion recommendation systems and image generation, enhancing both creativity and personalization. This thesis explores two key methodologies within these domains.


First, we introduce a **GAN Based Fashion Outfit Generator** for which we train a **StyleGAN2-ADA** model on the **Lookbook dataset** to generate realistic fashion images, achieving competitive performance. Using **GANSpace**, we identify and analyze latent space directions in an unsupervised manner, eliminating the need for labelled attributes and improving interpretability. The final model is deployed on **Hugging Face Spaces** with an interactive **Gradio UI**, enabling real-time exploration of generative fashion design.  

Second, we develop a **LightGBM-based Fashion recommender system** by integrating **collaborative filtering and gradient boosting (LightGBM)** to enhance personalization. Leveraging **text processing, dimensionality reduction, and similarity-based techniques**, we extract meaningful insights from the **H&M Fashion** and **Kaggle Fashion Product datasets**. We train two models: **User-User Collaborative Filtering (UUCF)** and **LightGBM**, evaluating their performance using **Mean Average Precision @ 12 (MAP@12)**. Our results demonstrate that **boosting techniques consistently outperform filtering-based methods**, underscoring their effectiveness in improving recommendation accuracy.  

Our findings highlight the transformative potential of **generative modelling for fashion synthesis** and **machine learning techniques for data-driven, personalized recommendations**, paving the way for more intelligent AI applications in fashion retail.


## Experiments
1. ### [GAN Based Fashion Outfit Generator](https://github.com/AdiNarendra98/AI-for-Fashion/tree/main/GAN%20Based%20Fashion%20Outfit%20Generator)
![teaser](https://github.com/AdiNarendra98/AI-for-Fashion/blob/main/ss/Guccio%20Ai.png)
- Using Generative Adversarial Networks, our model can generate clothing images and mix these images. While mixing, you can control which structure or style you want the clothing to copy. Additionally, you can edit the generated clothing with several given attributes such as dark colour, jacket, dress, or coat.

2. ### [Fashion Recommender Engine using LightGBM](https://github.com/AdiNarendra98/AI-for-Fashion/tree/main/Fashion%20Recommender%20Engine%20using%20LightGBM)
![iDresser](https://github.com/AdiNarendra98/AI-for-Fashion/blob/main/ss/iDresser.png)
- Using LightGBM, iDresser unlike the conventional systems that rely on the user's previous purchases and history, this project aims at using an image of a product given as input by the user to generate recommendations since many a time people see something that they are interested in and tend to look for products that are similar to that.


## Additional Experiments
 ### [What's this Called(Fashion Clothing Segmentation)](https://github.com/AdiNarendra98/AI-for-Fashion/tree/main/Additional%20Experiments/What's%20this%20Called(Fashion%20Clothing%20Segementation))
![WtCiF](https://github.com/AdiNarendra98/AI-for-Fashion/blob/main/ss/What's%20this%20Called.png)
- The system uses pixel-wise detection algorithms to detect various product categories in the user input image and then segments it to particular types of clothing like Tshirts, Pants, Jackets etc and further can be used to find similar products based on a certain kind of segmentation.

### [Rent the Fashion : A Rental Clothing Recommender System](https://github.com/AdiNarendra98/AI-for-Fashion/tree/main/Additional%20Experiments/Rent%20the%20Fashion(Rental%20Clothing%20Recommender))
![Rentit](https://github.com/AdiNarendra98/AI-for-Fashion/blob/main/ss/Rent%20the%20Fashion.png)
- A recommender system that recommends the clothes to the female customers for their rental purposes. The rental purposes depend on the activities a user wants to carry out, such as: vacation, meetings, weddings, dates, etc. The recommendation is based on features like customers’ height, weight, bust size, body type, age, and reason to rent.This improves costumer's experience and preserves trend in fashion.
<!-- * [License](#license) -->
