import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

const normalizeData = (data, key) => {
    const values = data.map(item => item[key]);
    const max = Math.max(...values);
    const min = Math.min(...values);
    return data.map(item => ({
        ...item,
        [key]: (item[key] - min) / (max - min),
    }));
};

const addLabel = (scene, text, position) => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = '48px serif';
    context.fillText(text, 10, 50);

    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(material);
    sprite.position.copy(position);
    sprite.scale.set(10, 5, 1); // Adjust as needed
    scene.add(sprite);
};

const ScatterPlot3D = () => {
    const mountRef = useRef(null);
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('/api/car-price-mileage')
            .then(response => response.json())
            .then(fetchedData => {
                console.log("Fetched data:", fetchedData);
                const normalizedData = ['mileage', 'price', 'year'].reduce(
                    (acc, key) => normalizeData(acc, key),
                    fetchedData
                );
                setData(normalizedData);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    useEffect(() => {
        if (data.length === 0) {
            return;
        }

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0d0d0d);
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        const mountCurrent = mountRef.current;
        mountCurrent.appendChild(renderer.domElement);

        data.forEach(point => {
            const geometry = new THREE.SphereGeometry(0.5, 32, 32);
            const material = new THREE.MeshBasicMaterial({ color: 0xFCF239 });
            const sphere = new THREE.Mesh(geometry, material);

            // Scale positions to fit within the scene better
            const x = point.mileage * 100 - 50; // Example scaling
            const y = point.price * 100 - 50;
            const z = point.year * 100 - 50;

            sphere.position.set(x, y, z);
            scene.add(sphere);

            // Add labels
            addLabel(scene, `M:${point.mileage.toFixed(2)}`, sphere.position);
        });

        camera.position.z = 150;

        const animate = function () {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        };

        animate();

        return () => {
            mountCurrent.removeChild(renderer.domElement);
        };
    }, [data]);

    return <div ref={mountRef} style={{ width: '100%', height: '100vh' }} />;
};

export default ScatterPlot3D;
