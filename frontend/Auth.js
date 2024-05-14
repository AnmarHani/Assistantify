import React, { useState } from 'react';
import { Button, TextInput, View, StyleSheet, Text, Image } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Auth = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = async () => {
    // Send sign in request to backend
    // For simplicity, let's assume the backend returns a token
    const token = 'your_token_from_backend';
    await AsyncStorage.setItem('userToken', token);
    navigation.replace('Home');
  };

  const handleSignUp = async () => {
    // Send sign up request to backend
    // For simplicity, let's assume the backend returns a token
    const token = 'your_token_from_backend';
    await AsyncStorage.setItem('userToken', token);
    navigation.replace('Home');
  };

  return (
    <View style={styles.container}>
      <Image style={styles.logo} source={require('./logo.png')} />
      <View style={styles.form}>
        <TextInput
          style={styles.input}
          onChangeText={setUsername}
          value={username}
          placeholder="Username"
          placeholderTextColor="#FFFFFF"
        />
        <TextInput
          style={styles.input}
          onChangeText={setPassword}
          value={password}
          placeholder="Password"
          placeholderTextColor="#FFFFFF"
          secureTextEntry
        />
        <View style={styles.buttonsContainer}>
          <Button title="Sign In" onPress={handleSignIn} color="#776BFF" />
          <Button title="Sign Up" onPress={handleSignUp} color="#776BFF" />
        </View>
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
  },
  logo: {
    width: 80,
    marginBottom: 20,
  },
  form: {
    width: '80%',
    backgroundColor: '#C54DEF',
    padding: 20,
    borderRadius: 10,
  },
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    color: '#FFFFFF',
    borderColor: '#FFFFFF',
    padding: 10,
    borderRadius: 60,
  },
  buttonsContainer: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around'
  },
});

export default Auth;
