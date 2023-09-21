// External imports
import { Button } from '@mui/material'
import { useEffect, useRef } from 'react'
import apis from '../../utils/axios/apis'



const GoogleAuth = ({ scope }) => {
    const googleButton = useRef(null);
    const client = useRef(null); // Use useRef to store the client

    useEffect(() => {
        const id = process.env.REACT_APP_GOOGLE_CLIENT
        /*global google*/
        if (scope) {
            client.current = google.accounts.oauth2.initCodeClient({
                client_id: id,
                ux_mode: 'popup',
                access_type: 'offline',
                scope: scope,
                callback: handleCredentialResponse,
            })
        }
        else {
            google.accounts.id.initialize({
                client_id: id,
                callback: handleCredentialResponse,
            })
            google.accounts.id.renderButton(
                googleButton.current,
                { theme: 'outline', size: 'large' }
            )
        }
        async function handleCredentialResponse(response) {
            if (scope) {
                // Send the response to your backend server.
                let scopes = scope.split(' ')
                await apis.post_code({ code: response.code, scopes: scopes })
                    .then(res => {
                        console.log(res.data)
                    })
                    .catch(err => { console.log(err) })
            }
            else {
                await apis.google_login({ credential: response.credential })
                .then(res => {
                    localStorage.setItem('access_token', res.data.access_token)
                    localStorage.setItem('refresh_token', res.data.refresh_token)
                    localStorage.setItem('user', JSON.stringify(res.data.user))
                })
                .catch(err => { console.log(err) })
                console.log(response)

            }

        }
    }, [scope])



    // Handle the button click event
    function handleButtonClick() {
        if (scope) {
            // Make the OAuth2 request using the `client.current` object
            console.log(client.current)
            client.current.requestCode();
            // client.current.Request();

        }
    }

    return (
        <>
            {scope ? (
                <Button onClick={handleButtonClick} >
                    authorize with oauth2
                </Button>
            ) : (
                <div ref={googleButton}></div>
            )}
        </>
    )
}

export default GoogleAuth
