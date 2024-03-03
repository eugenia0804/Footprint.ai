import os
import imageio

def create_gif(image_folder, gif_name, duration_seconds):
    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            images.append(imageio.imread(os.path.join(image_folder, filename)))
    
    # Reverse the order of images
    # images = images[::-1]
    
    duration_milliseconds = duration_seconds * 1000  # Convert seconds to milliseconds
    imageio.mimsave(gif_name, images, duration=duration_milliseconds)

# Example usage:
image_folder = 'word2vec/images/keyword-freq'
gif_name = 'word2vec/freq.gif'
duration_seconds = 1.2  # duration per frame in seconds (adjust for desired speed)

create_gif(image_folder, gif_name, duration_seconds)
