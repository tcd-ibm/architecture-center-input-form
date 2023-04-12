import { Button, Form, Stack, TextInput } from '@carbon/react';
import { Add } from '@carbon/icons-react';
import { useRef } from 'react';

function AddTagForm(props) {
    const { onSubmit = () => {} } = props;

    const inputRef = useRef();

    const submitHandler = () => {
        if(inputRef.current.value) {
            onSubmit(inputRef.current.value);
            inputRef.current.value = '';
        }
    };

    return (
        <Form style={{marginTop: '20px', width: '100%'}}>
            <Stack orientation='horizontal' gap={6}>
                <TextInput size='sm' labelText='Tag name' ref={inputRef} />
                <div style={{width: 'fit-content', height: 'fit-content', marginTop: 'auto'}} >
                    <Button size='sm' renderIcon={Add} hasIconOnly iconDescription='Add' onClick={submitHandler} />
                </div>
            </Stack>
        </Form>
    );
}

export default AddTagForm;