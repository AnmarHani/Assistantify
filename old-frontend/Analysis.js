import React, { useEffect, useState } from 'react';
import { Image, View, StyleSheet } from 'react-native';
import config from './config';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Analysis = () => {
  const [images, setImages] = useState([]);


  useEffect(async () => {
    const token = await AsyncStorage.getItem('userToken');
    fetch(config.url + '/analysis', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const prefixedImages = data.images.map(image => 'data:image/png;base64,' + image);
        setImages(prefixedImages);
      });
  }, []);

  return (
    <View style={styles.container}>
      {images.map((image, index) => (
        <Image key={index} style={styles.image} source={{ uri: image }} />
      ))}
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
  image: {
    width: '100%',
    height: 200,
    resizeMode: 'contain',
  },
});

export default Analysis;
