# Sam Freund
# Lab 11
# CSC 2611

---

## Part 1

### VGG16 Overview
VGG16 is a deep convolutional neural network developed by the Visual Geometry Group at Oxford, known for its simple, uniform architecture composed of stacked 3×3 convolutional layers and 2×2 max-pooling layers. It has 16 weight layers and was designed to test how increasing network depth affects performance. VGG16 was trained on the ImageNet Large Scale Visual Recognition Challenge (ILSVRC) dataset, which contains over 1.2 million labeled images across 1,000 object categories. As a result, VGG16 learns rich, hierarchical visual features—edges, textures, shapes, and object parts—making it effective for image classification and useful as a feature extractor for transfer learning.

### srun

srun --gpus=1 --cpus-per-gpu=8 singularity exec --nv -B /data:/data /data/containers/msoe-tensorflow-20.07-tf2-py3.sif python /home/ad.msoe.edu/freunds/classes/2611/lab11/Lab11.py --data /data/cs2300/L9/fruits --batch_size 8 --epochs 10 –main_dir /home/ad.msoe.edu/freunds/classes/2611/lab11 --augment_data false –fine_tune false


## Part 2

42 accurate predictions out of 50 images for freshapples. Accuracy: 0.84
48 accurate predictions out of 49 images for freshbanana. Accuracy: 0.9795918367346939
42 accurate predictions out of 43 images for freshoranges. Accuracy: 0.9767441860465116
68 accurate predictions out of 74 images for rottenapples. Accuracy: 0.918918918918919
67 accurate predictions out of 68 images for rottenbanana. Accuracy: 0.9852941176470589
17 accurate predictions out of 45 images for rottenoranges. Accuracy: 0.37777777777777777


## Part 3

I find this to be much simpler than typing out the entire srun command. However, this is (in my opinion) a bit less persistent as the history of the `.sh` file isn't tracked, while the previous srun command can be found using `history`.

Running `lab11.sh`, we use hyperparameters batch_size=32 and epochs=5. Results of the final epoch can be found below. \
`37/36 - 25s - loss: 0.1809 - accuracy: 0.9349 - val_loss: 0.2246 - val_accuracy: 0.9179`



## Part 4
For testing different parameters, I used a grid search running on a slurm array, implemented with the below script.

```bash
#!/bin/bash
#SBATCH --partition=teaching
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --cpus-per-gpu=20
#SBATCH --error='sbatcherrorfile_%A_%a.out'
#SBATCH --output='sbatchoutputfile_%A_%a.out'
#SBATCH --time=0-2:0
# Array job setup - adjust based on grid search size
#SBATCH --array=0-11

####
# Grid search parameters
####
# Define batch sizes to search over
batch_sizes=(16 32 64 128 256)
# Define epochs to search over
epochs_values=(5 10 15 20)

# Calculate total combinations
num_batch_sizes=${#batch_sizes[@]}
num_epochs=${#epochs_values[@]}

# Map array task ID to parameter combination
batch_idx=$((SLURM_ARRAY_TASK_ID / num_epochs))
epoch_idx=$((SLURM_ARRAY_TASK_ID % num_epochs))

# Get current parameters
current_batch_size=${batch_sizes[$batch_idx]}
current_epochs=${epochs_values[$epoch_idx]}

echo "Running experiment with batch_size=$current_batch_size and epochs=$current_epochs"
echo "Job ID: $SLURM_ARRAY_JOB_ID, Task ID: $SLURM_ARRAY_TASK_ID"

####
# Job execution
####
# Path to container
container="/data/containers/msoe-tensorflow-20.07-tf2-py3.sif"

# Command to run inside container
command="python Lab11.py --data /data/cs2300/L9/fruits --batch_size $current_batch_size --epochs $current_epochs --main_dir /home/ad.msoe.edu/freunds/classes/2611/lab11 --augment_data true --fine_tune false"

# Execute singularity container on node
singularity exec --nv -B /data:/data ${container} /usr/local/bin/nvidia_entrypoint.sh ${command}
```

The first set of runs I tested batch sizes up to 128 and epochs up to 15. I found that this did not result in high enough accuracy, so I added another value to each list and reran. I found that increasing epochs helped me get closer, but increasing batch size was not helpful. The best value from that run was 0.972, using a batch size of 16 and running 20 epochs. The third run used batch sizes of 12, 16, 20, and 24; with epochs 14, 16, 18, 20.