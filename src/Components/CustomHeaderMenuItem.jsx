import { useNavigate } from 'react-router';
import { HeaderMenuItem } from '@carbon/react';

function CustomHeaderMenuItem(props) {
    const { href, children, ...remainingProps } = props;

    const navigate = useNavigate();

    return (
        <HeaderMenuItem 
            onClick={() => navigate(href)}
            style={{cursor: 'pointer'}}
            {...remainingProps}
        >
            {children}
        </HeaderMenuItem>
    );
}

export default CustomHeaderMenuItem;