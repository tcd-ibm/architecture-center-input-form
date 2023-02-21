import { useState } from 'react';

import AuthContext from './AuthContext';

function AuthContextProvider(props) {
    const [user, setUser] = useState(null);

    return (
        <AuthContext.Provider value={[user, setUser]}>
            {props.children}
        </AuthContext.Provider>
    );
}

export default AuthContextProvider;