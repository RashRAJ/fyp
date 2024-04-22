import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DrowsinessLevel = () => {
    const [level, setLevel] = useState('None');

    useEffect(() => {
        const interval = setInterval(() => {
            axios.get('http://127.0.0.1:5000/drowsiness_level')
                .then(response => {
                    setLevel(response.data.level);
                })
                .catch(error => console.error('Error fetching drowsiness level:', error));
        }, 10000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <h2>Drowsiness Level</h2>
            <p>{level}</p>
        </div>
    );
};

export default DrowsinessLevel;
