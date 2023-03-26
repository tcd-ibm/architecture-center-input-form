import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import qs from 'qs';

import User from '@/utils/User';

const LOCAL_STORAGE_USER_OBJECT_KEY = 'authUserObject';

const AuthContext = createContext([null, () => {}]);

function useAuth() {
    const [user, setUser] = useContext(AuthContext);

    const login = async ({ email, password }, { persist } = {}) => {
        const requestData = {
            username: email,
            password: password
        };

        const response = await axios.post('/user/token', qs.stringify(requestData));

        if(persist) {
            try {
                localStorage.setItem(LOCAL_STORAGE_USER_OBJECT_KEY, JSON.stringify(
                    new User(response.data.access_token, response.data.role)
                ));
            } catch(error) {
                // write to localStorage failed, saving just in local state
            }
        }
        setUser(new User(response.data.access_token, response.data.role));
    };

    const signup = async ({ email, username, password }) => {
        const requestData = {
            email: email,
            username: username,
            password: password
        };

        const response = await axios.post('/user/signup', requestData, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } });
        setUser(new User(response.data.access_token, response.data.role));
    };

    const logout = () => {
        localStorage.removeItem(LOCAL_STORAGE_USER_OBJECT_KEY);
        setUser(null);
    };

    return {
        get user() {
            if(user) return user;
            const storedUserData = JSON.parse(localStorage.getItem(LOCAL_STORAGE_USER_OBJECT_KEY));
            if(!storedUserData) return null;
            const storedUser = Object.setPrototypeOf(storedUserData, User.prototype);
            return storedUser;
        },
        login,
        signup,
        logout
    };
}

function AuthContextProvider(props) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        if(!user) {
            const storedUserData = JSON.parse(localStorage.getItem(LOCAL_STORAGE_USER_OBJECT_KEY));
            if(storedUserData) {
                const storedUser = Object.setPrototypeOf(storedUserData, User.prototype);
                setUser(storedUser);
            }
        }
    }, [user, setUser]);

    return (
        <AuthContext.Provider value={[user, setUser]}>
            {props.children}
        </AuthContext.Provider>
    );
}

export default useAuth;
export { AuthContextProvider };