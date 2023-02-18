import { forwardRef } from "react";
import { Link } from "@carbon/react";

import LoginFormGeneric from "./LoginFormGeneric";

function LoginFormPasswordStep(props, ref) {
    const { email, onSubmit } = props;

    const componentProps = {
        subheadingContentNode: <>Logging in as {email} <Link href='/login'>Not you?</Link></>,
        inputType: 'password',
        rememberIdCheckbox: false,
        buttonText: `Log in`,
        onSubmit: onSubmit
    };

    return (
        <LoginFormGeneric {...componentProps} ref={ref} />
    );
}

LoginFormPasswordStep = forwardRef(LoginFormPasswordStep);

export default LoginFormPasswordStep;