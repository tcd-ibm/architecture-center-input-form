import { createContext, useContext, useState } from 'react';
import axios from 'axios';
import qs from 'qs';

import User from '@/utils/User';

const AuthContext = createContext();

function useAuth() {
    const [user, setUser] = useContext(AuthContext);

    const login = async ({ email, password }, { persist } = {}) => {
        const requestData = {
            username: email,
            password: password
        };

        const response = await axios.post('/user/token', qs.stringify(requestData));
        setUser(new User(response.data.access_token));
    };

    const signup = async ({ email, username, password }) => {
        const requestData = {
            email: email,
            username: username,
            password: password
        };

        const response = await axios.post('/user/signup', requestData, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } });
        setUser(new User(response.data.access_token));
    };

    const logout = () => {
        setUser(null);
    };

    return {
        user,
        login,
        signup,
        logout
    };
}

function AuthContextProvider(props) {
    const [user, setUser] = useState(null);

    return (
        <AuthContext.Provider value={[user, setUser]}>
            {props.children}
        </AuthContext.Provider>
    );
}

export default useAuth;
export { AuthContextProvider };