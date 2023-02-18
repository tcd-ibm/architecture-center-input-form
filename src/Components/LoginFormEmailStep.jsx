import { forwardRef } from "react";
import { Link } from "@carbon/react";

import LoginFormGeneric from "./LoginFormGeneric";

function LoginFormEmailStep(props, ref) {
    const { onSubmit } = props;

    const componentProps = {
        subheadingContentNode: <>Don't have an account? <Link href='/signup'>Sign up</Link></>,
        inputType: 'email',
        rememberIdCheckbox: true,
        buttonText: `Continue`,
        onSubmit: onSubmit
    };

    return (
        <LoginFormGeneric {...componentProps} ref={ref} />
    );
}

LoginFormEmailStep = forwardRef(LoginFormEmailStep);

export default LoginFormEmailStep;