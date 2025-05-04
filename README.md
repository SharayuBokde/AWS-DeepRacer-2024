# AWS-DeepRacer-2024

This repository contains code, configuration, and training logs for AWS DeepRacer competition held at JPMorgan Chase & Co. Mumbai Tech Centre. 
AWS DeepRacer is a 1/18th scale autonomous racing car designed to test reinforcement learning (RL) models.

## Project Overview

The goal of this project is to create a reinforcement learning model capable of autonomously navigating a virtual track in the AWS DeepRacer console. This involves:

1. Developing a reward function.
2. Configuring training parameters.
3. Training the model in the AWS DeepRacer simulator.
4. Testing and fine-tuning the model.

## Key Features

- **Reinforcement Learning**: Using AWS SageMaker to train the model.
- **Simulation**: Testing in a virtual environment before deploying to the physical car.
- **Custom Reward Function**: Designing and implementing a custom reward function for optimal performance.
- **Track Evaluation**: Analyzing performance on multiple tracks.

## Prerequisites

To replicate or contribute to this project, ensure you have the following:

1. AWS Account with access to AWS DeepRacer.
2. Basic knowledge of Python and Reinforcement Learning.
3. An understanding of the AWS DeepRacer environment.

## Reward Function

The reward function plays a crucial role in training your DeepRacer model. Below is an example of the reward function used in this project:

## Training Configuration

The `training_config.json` file specifies parameters such as the learning rate, batch size, and number of episodes for training:

```json
{
  "batch_size": 64,
  "num_epochs": 10,
  "learning_rate": 0.001,
  "exploration": {
    "start_epsilon": 1.0,
    "end_epsilon": 0.1,
    "decay_steps": 1000
  }
}
```

## Training and Evaluation

1. **Training**:
   - Upload the reward function and configuration to the AWS DeepRacer console.
   - Start training in the AWS simulator.

2. **Evaluation**:
   - Use the "Evaluate" option to test the model on a specific track.
   - Record and analyze performance metrics.

## Results

Include graphs and metrics showcasing model performance over time. For example:

- **Training Progress**: Mean reward per episode.
- **Track Performance**: Completion rate and lap time.

## Future Improvements

- Fine-tuning the reward function for complex tracks.
- Adding new features, such as dynamic obstacle avoidance.
- Deploying the model to a physical DeepRacer car.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- AWS DeepRacer Team
- Reinforcement Learning Community
- OpenAI for inspiring RL enthusiasts worldwide
