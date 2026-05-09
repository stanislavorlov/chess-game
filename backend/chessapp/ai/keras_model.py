import os
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
from .bitboards import Bitboards

class ChessZeroModel:
    def __init__(self, weights_path=None):
        self.model = self._build_model()
        if weights_path and os.path.exists(weights_path):
            self.model.load_weights(weights_path)
            
    def _build_model(self):
        # Input shape: 8x8 squares, 12 channels (6 piece types * 2 colors)
        inputs = layers.Input(shape=(8, 8, 12))
        
        # Initial Convolutional Block
        x = layers.Conv2D(64, kernel_size=(3, 3), padding='same')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        
        # Residual Blocks
        for _ in range(5): # 5 blocks for a lightweight version
            res = x
            x = layers.Conv2D(64, kernel_size=(3, 3), padding='same')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Activation('relu')(x)
            x = layers.Conv2D(64, kernel_size=(3, 3), padding='same')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Add()([x, res])
            x = layers.Activation('relu')(x)
            
        # Policy Head
        policy = layers.Conv2D(2, kernel_size=(1, 1), padding='same')(x)
        policy = layers.BatchNormalization()(policy)
        policy = layers.Activation('relu')(policy)
        policy = layers.Flatten()(policy)
        policy = layers.Dense(4096, activation='softmax', name='policy')(policy)
        
        # Value Head
        value = layers.Conv2D(1, kernel_size=(1, 1), padding='same')(x)
        value = layers.BatchNormalization()(value)
        value = layers.Activation('relu')(value)
        value = layers.Flatten()(value)
        value = layers.Dense(64, activation='relu')(value)
        value = layers.Dense(1, activation='tanh', name='value')(value)
        
        model = models.Model(inputs=inputs, outputs=[policy, value])
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss={'policy': 'categorical_crossentropy', 'value': 'mean_squared_error'}
        )
        return model

    def predict(self, bb: Bitboards):
        """
        Converts Bitboards to a tensor and predicts policy and value.
        """
        tensor = self._bitboards_to_tensor(bb)
        # Add batch dimension
        tensor = np.expand_dims(tensor, axis=0)
        policy, value = self.model.predict(tensor, verbose=0)
        # Flatten outputs
        return policy[0], value[0][0]

    def _bitboards_to_tensor(self, bb: Bitboards) -> np.ndarray:
        """
        Converts Bitboards to an 8x8x12 tensor.
        """
        tensor = np.zeros((8, 8, 12), dtype=np.float32)
        
        bb_maps, _, _ = bb.generate_maps()
        # Order matters for the neural network consistently:
        # P, N, B, R, Q, K for White (0-5)
        # P, N, B, R, Q, K for Black (6-11)
        
        keys = list(bb_maps.keys())
        # Sort by Side, then PieceType (which are IntEnums)
        keys.sort(key=lambda k: (k[0], k[1]))
        
        for channel, key in enumerate(keys):
            board = bb_maps[key]
            for sq in range(64):
                if (board >> sq) & 1:
                    row = 7 - (sq // 8) # Rank 8 is row 0
                    col = sq % 8        # File A is col 0
                    tensor[row, col, channel] = 1.0
                    
        return tensor
