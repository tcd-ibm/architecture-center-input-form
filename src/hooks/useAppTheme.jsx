import { createContext, useContext, useState } from 'react';
import { Helmet } from 'react-helmet';
import { Theme } from '@carbon/react';

const AppThemeContext = createContext([null, () => {}]);

function useAppTheme() {
    const [theme, setTheme] = useContext(AppThemeContext);
    return [theme, setTheme];
}

function AppThemeProvider(props) {
    const [theme, setTheme] = useState('white');

    return (
        <AppThemeContext.Provider value={[theme, setTheme]}>
            <Theme theme={theme}>
                {
                    theme === 'g100' &&
                    <Helmet>
                        <style>{'body { background-color: #161616; }'}</style> 
                    </Helmet>
                }
                {props.children}
            </Theme>
        </AppThemeContext.Provider>
    );
}

export default useAppTheme;
export { AppThemeProvider };