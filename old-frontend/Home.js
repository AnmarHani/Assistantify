import React, { useState } from 'react';
import {
  Button,
  TextInput,
  View,
  StyleSheet,
  Text,
  ScrollView,
  Image,
} from 'react-native';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';
import config from './config'
import AsyncStorage from '@react-native-async-storage/async-storage';

const Home = () => {
  const [coins, setCoins] = useState('0');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [recording, setRecording] = useState(false);

  const handleSend = async() => {
    const token = await AsyncStorage.getItem('userToken');
    // Send message to backend
    fetch(config.url + '/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token
      },
      body: JSON.stringify({ message }),
    })
      .then((response) => response.json())
      .then((data) => {
        setMessages([
          ...messages,
          { user: 'You', text: message },
          { user: 'Bot', text: data.response },
        ]);
        setMessage('');
        setCoins(data.coins);
      });
  };

  const handlePlay = async (uri) => {
    const soundObject = new Audio.Sound();
    try {
      await soundObject.loadAsync({ uri });
      await soundObject.playAsync();
    } catch (error) {
      console.log(error);
    }
  };

  const handleVoice = async () => {
    const token = await AsyncStorage.getItem('userToken');

    if (!recording) {
      // Start recording
      console.log('Requesting permissions..');
      const { status } = await Audio.requestPermissionsAsync();
      if (status !== 'granted') {
        throw new Error('Permissions not granted');
      }
      const newRecording = new Audio.Recording();
      await newRecording.prepareToRecordAsync(
        Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
      );
      await newRecording.startAsync();
      setRecording(newRecording);
    } else {
      // Stop recording and send to backend
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      const fileBase64 = await FileSystem.readAsStringAsync(uri, {
        encoding: FileSystem.EncodingType.Base64,
      });
      fetch(config.url + '/voice', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token
        },
        body: JSON.stringify({ file: fileBase64 }),
      })
        .then((response) => response.json())
        .then((data) => {
          const audioBase64 = data.response;
          const audioUri = FileSystem.cacheDirectory + 'response.mp3';
          FileSystem.writeAsStringAsync(audioUri, audioBase64, {
            encoding: FileSystem.EncodingType.Base64,
          });
          setMessages([
            ...messages,
            { user: 'You', text: data.user_message },
            { user: 'Bot', text: data.system_message },
          ]);
          setCoins(data.coins);
          handlePlay(audioUri);
        });
      setRecording(null);
    }
  };

  return (
    <View style={styles.container}>
    <View style={styles.header}>
      <Image style={styles.logo} source={require('./logo.png')} />
      <View style={styles.coinContainer}>
        <Text style={styles.coinText}>ATN</Text>
        <Image style={styles.coinIcon} source={require('./assistantoin.png')} />
        <Text style={styles.coinText}>{coins}</Text>
      </View>
    </View>

      <ScrollView style={styles.chatContainer}>
        {messages.map((message, index) => (
          <Text key={index} style={styles.message(message.user)}>
            {message.user}: {message.text}
          </Text>
        ))}
      </ScrollView>
      <TextInput
        style={styles.input}
        onChangeText={setMessage}
        value={message}
        placeholder="Type your message here..."
        placeholderTextColor="#C54DEF"
      />
      <View style={styles.buttonContainer}>
        <Button
          title={recording ? 'Stop Recording' : 'Start Recording'}
          onPress={handleVoice}
          color="#C54DEF"
        />
        <Button title="Send" onPress={handleSend} color="#C54DEF" />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    alignItems: 'center',
    justifyContent: 'center',
      paddingTop: 20,
  },
  logo: {
    width: 80,
  },
  chatContainer: {
    flex: 1,
    width: '100%',
    padding: 10,
  },
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    color: '#C54DEF',
    borderColor: '#C54DEF',
    padding: 10,
    borderRadius: 60,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginBottom: 20,
  },
  header: {
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
  width: '100%',
  paddingHorizontal: 10,
},
coinContainer: {
  flexDirection: 'row',
  alignItems: 'center',
},
coinIcon: {
  width: 30,
  height: 30,
},
coinText: {
  color: '#ffffff',
  marginLeft: 5,
},

  message: (user) => ({
    color: user === 'You' ? '#C54DEF' : '#fff',
  }),
});

export default Home;
