# GAN-Based Fashion Outfit Generator

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/mfrashad/ClothingGAN)

## Inspiration
GAN or Generative Adversarial Network is a generative model that able to generate images by learning the probability distribution of a large image dataset. I always find GANs fascinating as it enables me to generate high-quality arts or design even without the technical or artistic skill in drawing. Recently, I've seen many face editing demonstrations on GAN, but never seen semantic manipulation in other datasets. Hence,  I created ClothingGAN an application where you can collaboratively design clothes without high technical expertise.

## What it does
Our model is able to generate clothing images and mix these images. While mixing, you can control which structure or style that you want the clothing to copy. Additionally, you can edit the generated clothing with several given attributes such as dark color, jacket, dress, or coat.

## How I built it
I trained StyleGAN2-ADA on a subset of the Lookbook dataset. The total images I trained it on are 8,726 clothing images with a clean background. I transfer learned from FFHQ model and trained the model for a day.

After finished training the GAN, I proceeded to use GANSpace method to find important directions in the latent space. Then, I tried to guess what these directions represent and labeled them accordingly. The reason I use GANSpace is that it is unsupervised and does not need an attribute classifier.

Finally, I created a UI with Gradio UI library. All the development is done on Colab. Gradio made deployment very easy. I can directly deploy the UI from Colab where Gradio will create a proxy from the Colab server to their domain and the given URL, hence allowing the general public to use the UI or demo. However, since I cannot keep the Colab server on continuously due to GPU usage, ping me if you want to try out the demo.


