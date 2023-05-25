import axios from 'axios';

const dev = process.env.NODE_ENV !== 'production';
export const url = dev
    ? 'http://172.26.135.213:80/api'
    : 'http://172.26.135.213:80/api';


const instance = axios.create({
    baseURL: url,
    headers: {
        'Content-Type': 'application/json'
    }
});

export function handleLogin(token) {
    instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

//instance.defaults.withCredentials = true;

export default instance;
