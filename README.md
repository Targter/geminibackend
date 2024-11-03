

## Usage



Once the server is running, you can use the API to convert text into real-time streaming audio. This can be integrated into web or mobile applications for interactive voice responses.



## API Endpoints



### GET /stream/<text>



Stream audio generated from text in real-time.



- **URL:** `/stream/<text>`

- **Method:** `GET`

- **URL Parameters:**

  - `text` (string): The text you want to convert to speech.

- **Response:**

  - Audio stream in `audio/wav` format.



**Example:**

```bash

curl https://ttserver-psi.vercel.app/stream/Hello%20world

```



## Example Implementation



Here's how you might implement a simple HTML audio player to interact with the API.



### Web (HTML + JavaScript)

```html

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="UTF-8">

  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Real-Time TTS</title>

</head>

<body>

  <h1>Text-to-Speech Streaming</h1>

  <input type="text" id="inputText" placeholder="Enter text to speak">

  <button onclick="playAudio()">Play</button>

  <audio id="audioPlayer" controls></audio>



  <script>

    function playAudio() {

      const text = document.getElementById("inputText").value;

      const audioPlayer = document.getElementById("audioPlayer");

      audioPlayer.src = `https://ttserver-psi.vercel.app/stream/${encodeURIComponent(text)}`;

      audioPlayer.play();

    }

  </script>

</body>

</html>

```



### Mobile (React Native + Expo Audio)

```javascript

import React, { useState } from 'react';

import { View, TextInput, Button } from 'react-native';

import { Audio } from 'expo-av';



export default function App() {

  const [text, setText] = useState('');

  const [sound, setSound] = useState();



  async function playAudio() {

    const sound = new Audio.Sound();

    try {

      await sound.loadAsync({ uri: `https://ttserver-psi.vercel.app/stream/${encodeURIComponent(text)}` });

      await sound.playAsync();

    } catch (error) {

      console.log("Error playing audio:", error);

    }

  }



  return (

    <View>

      <TextInput

        placeholder="Enter text to speak"

        onChangeText={setText}

        value={text}

      />

      <Button title="Play" onPress={playAudio} />

    </View>

  );

}

```




### Explanation

- **Installation**: Details on setting up the environment and dependencies.

- **Usage**: Instructions on using the API endpoint.

- **API Endpoints**: Defines the `/stream/<text>` endpoint with parameters, response format, and a curl example.

- **Example Implementation**: Provides sample code for integrating with both web (HTML + JavaScript) and mobile (React Native) environments.



This documentation should help users integrate the TTS streaming API in their projects easily.
