import React, {useState} from 'react';
import {Button, Theme} from '@carbon/react';
import {Helmet} from 'react-helmet';

import MainHeader from '@/Components/MainHeader';

function SettingsPage() {

    const stored = localStorage.getItem('toggleDarkMode');
    const [toggleDarkMode, setToggleDarkMode] = useState(
          stored === 'true' ? true : false);
        
    const color=(toggleDarkMode ? '161616': 'white');

    return (
        <>
            <Theme theme ={stored==='true' ? 'g100' : 'white'}>
                <Helmet>
                    <style>{'body { background-color:#'+ color + '; }'}</style> 
                </Helmet>
                <MainHeader/>           
                <div style= {{top:70, left:20, position:'fixed'}}>
                    <Button kind='primary' onClick={() => {
                        setToggleDarkMode(!toggleDarkMode);
                        localStorage.setItem('toggleDarkMode', !toggleDarkMode);
                    }}>
                        Change Mode
                    </Button>
                </div>
            </Theme>
        </>
    );
}

export default SettingsPage; 