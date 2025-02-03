import nltk; nltk.download('wordnet')

#@title Load Model
selected_model = 'lookbook'

# Load model
import torch
import PIL
import numpy as np
from PIL import Image
import imageio
from models import get_instrumented_model
from decomposition import get_or_compute
from config import Config
from skimage import img_as_ubyte
import gradio as gr
import numpy as np
from ipywidgets import fixed

# Speed up computation
torch.autograd.set_grad_enabled(False)
torch.backends.cudnn.benchmark = True

# Specify model to use
config = Config(
  model='StyleGAN2',
  layer='style',
  output_class=selected_model,
  components=80,
  use_w=True,
  batch_size=5_000, # style layer quite small
)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

inst = get_instrumented_model(config.model, config.output_class,
                              config.layer, torch.device(device), use_w=config.use_w)

path_to_components = get_or_compute(config, inst)

model = inst.model

comps = np.load(path_to_components)
lst = comps.files
latent_dirs = []
latent_stdevs = []

load_activations = False

for item in lst:
    if load_activations:
      if item == 'act_comp':
        for i in range(comps[item].shape[0]):
          latent_dirs.append(comps[item][i])
      if item == 'act_stdev':
        for i in range(comps[item].shape[0]):
          latent_stdevs.append(comps[item][i])
    else:
      if item == 'lat_comp':
        for i in range(comps[item].shape[0]):
          latent_dirs.append(comps[item][i])
      if item == 'lat_stdev':
        for i in range(comps[item].shape[0]):
          latent_stdevs.append(comps[item][i])


#@title Define functions


# Taken from https://github.com/alexanderkuk/log-progress
def log_progress(sequence, every=1, size=None, name='Items'):
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    progress.value = index
                    label.value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )

def name_direction(sender):
  if not text.value:
    print('Please name the direction before saving')
    return
    
  if num in named_directions.values():
    target_key = list(named_directions.keys())[list(named_directions.values()).index(num)]
    print(f'Direction already named: {target_key}')
    print(f'Overwriting... ')
    del(named_directions[target_key])
  named_directions[text.value] = [num, start_layer.value, end_layer.value]
  save_direction(random_dir, text.value)
  for item in named_directions:
    print(item, named_directions[item])

def save_direction(direction, filename):
  filename += ".npy"
  np.save(filename, direction, allow_pickle=True, fix_imports=True)
  print(f'Latent direction saved as {filename}')

def mix_w(w1, w2, content, style):
    for i in range(0,5):
        w2[i] = w1[i] * (1 - content) + w2[i] * content

    for i in range(5, 16):
        w2[i] = w1[i] * (1 - style) + w2[i] * style
    
    return w2

def display_sample_pytorch(seed, truncation, directions, distances, scale, start, end, w=None, disp=True, save=None, noise_spec=None):
    # blockPrint()
    model.truncation = truncation
    if w is None:
        w = model.sample_latent(1, seed=seed).detach().cpu().numpy()
        w = [w]*model.get_max_latents() # one per layer
    else:
        w = [np.expand_dims(x, 0) for x in w]
    
    for l in range(start, end):
      for i in range(len(directions)):
        w[l] = w[l] + directions[i] * distances[i] * scale
    
    torch.cuda.empty_cache()
    #save image and display
    out = model.sample_np(w)
    final_im = Image.fromarray((out * 255).astype(np.uint8)).resize((500,500),Image.LANCZOS)
    
    
    if save is not None:
      if disp == False:
        print(save)
      final_im.save(f'out/{seed}_{save:05}.png')
    if disp:
      display(final_im)
    
    return final_im

def generate_mov(seed, truncation, direction_vec, scale, layers, n_frames, out_name = 'out', noise_spec = None, loop=True):
  """Generates a mov moving back and forth along the chosen direction vector"""
  # Example of reading a generated set of images, and storing as MP4.
  movieName = f'{out_name}.mp4'
  offset = -10
  step = 20 / n_frames
  imgs = []
  for i in log_progress(range(n_frames), name = "Generating frames"):
    print(f'\r{i} / {n_frames}', end='')
    w = model.sample_latent(1, seed=seed).cpu().numpy()

    model.truncation = truncation
    w = [w]*model.get_max_latents() # one per layer
    for l in layers:
      if l <= model.get_max_latents():
          w[l] = w[l] + direction_vec * offset * scale

    #save image and display
    out = model.sample_np(w)
    final_im = Image.fromarray((out * 255).astype(np.uint8))
    imgs.append(out)
    #increase offset
    offset += step
  if loop:
    imgs += imgs[::-1]
  with imageio.get_writer(movieName, mode='I') as writer:
    for image in log_progress(list(imgs), name = "Creating animation"):
        writer.append_data(img_as_ubyte(image))


#@title Demo UI


def generate_image(seed1, seed2, content, style, truncation, c0, c1, c2, c3, c4, c5, c6, start_layer, end_layer):
    seed1 = int(seed1)
    seed2 = int(seed2)

    scale = 1
    params = {'c0': c0,
          'c1': c1,
          'c2': c2,
          'c3': c3,
          'c4': c4,
          'c5': c5,
          'c6': c6}

    param_indexes = {'c0': 0,
              'c1': 1,
              'c2': 2,
              'c3': 3,
              'c4': 4,
              'c5': 5,
              'c6': 6}

    directions = []
    distances = []
    for k, v in params.items():
        directions.append(latent_dirs[param_indexes[k]])
        distances.append(v)

    w1 = model.sample_latent(1, seed=seed1).detach().cpu().numpy()
    w1 = [w1]*model.get_max_latents() # one per layer
    im1 = model.sample_np(w1)

    w2 = model.sample_latent(1, seed=seed2).detach().cpu().numpy()
    w2 = [w2]*model.get_max_latents() # one per layer
    im2 = model.sample_np(w2)
    combined_im = np.concatenate([im1, im2], axis=1)
    input_im = Image.fromarray((combined_im * 255).astype(np.uint8))
    

    mixed_w = mix_w(w1, w2, content, style)
    return input_im, display_sample_pytorch(seed1, truncation, directions, distances, scale, int(start_layer), int(end_layer), w=mixed_w, disp=False)

truncation = gr.Slider(minimum=0, maximum=1, value=0.5, label="Truncation")
start_layer = gr.Number(value=3, label="Start Layer")
end_layer = gr.Number(value=14, label="End Layer")
seed1 = gr.Number(value=0, label="Seed 1")
seed2 = gr.Number(value=0, label="Seed 2")
content = gr.Slider(label="Structure", minimum=0, maximum=1, value=0.5)
style = gr.Slider(label="Style", minimum=0, maximum=1, value=0.5)

slider_max_val = 20
slider_min_val = -20
slider_step = 1

c0 = gr.Slider(label="Sleeve & Size", minimum=slider_min_val, maximum=slider_max_val, value=0)
c1 = gr.Slider(label="Dress - Jacket", minimum=slider_min_val, maximum=slider_max_val, value=0)
c2 = gr.Slider(label="Female Coat", minimum=slider_min_val, maximum=slider_max_val, value=0)
c3 = gr.Slider(label="Coat", minimum=slider_min_val, maximum=slider_max_val, value=0)
c4 = gr.Slider(label="Graphics", minimum=slider_min_val, maximum=slider_max_val, value=0)
c5 = gr.Slider(label="Dark", minimum=slider_min_val, maximum=slider_max_val, value=0)
c6 = gr.Slider(label="Less Cleavage", minimum=slider_min_val, maximum=slider_max_val, value=0)



scale = 1

inputs = [seed1, seed2, content, style, truncation, c0, c1, c2, c3, c4, c5, c6, start_layer, end_layer]
description = "Change the seed number to generate different parent design. Made by <a href='https://github.com/AdiNarendra98' target='_blank'>Aditya</a>."

gr.Interface(generate_image, inputs, ["image", "image"], description=description, live=True, title="ClothingGAN").launch()