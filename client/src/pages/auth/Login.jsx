import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import apis from '../../utils/axios/apis'
import { toast } from "react-toastify";
import { useState } from 'react';
import GoogleAuth from './GoogleAuth';



function Copyright(props) {
    return (
        <Typography variant="body2" color="text.secondary" align="center" {...props}>
            {'Copyright © '}
            <Link color="inherit" href="https://mui.com/">
                Your Website
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}


export default function Login() {

    const [data, setData] = useState({ username: '', password: '' })

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (data.username === '' || data.password === '') {
            toast.error('Please fill all the fields')
            return
        }
        await apis.login(data)
            .then(res => {
                if (res.status === 200) {
                    localStorage.setItem('access_token', res.data.access_token)
                    localStorage.setItem('refresh_token', res.data.refresh_token)

                }

            })
            .catch(err => {
                toast.error(err)
                console.log(err)
            })
    };


    return (
        <div style={{
            display: 'flex',
            height: '100vh',
            alignItems: 'center',
        }}>

            <Container component="main" maxWidth="xs" >
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            onChange={(e) => { setData({ ...data, username: e.target.value }) }}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            onChange={(e) => { setData({ ...data, password: e.target.value }) }}
                        />
                        <FormControlLabel
                            control={<Checkbox value="remember" color="primary" />}
                            label="Remember me"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Sign In
                        </Button>

                        <div 

                        
                        
                        style={{
                            display: 'flex',
                            justifyContent: 'space-around',
                            alignItems: 'center',
                            width: '100%',
                            margin: '10px 0'
                        }}>
                        {/* Sign in with Google */}
                        <GoogleAuth />
                        <GoogleAuth scope = {'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/calendar openid https://www.googleapis.com/auth/userinfo.profile'} />
                        
                        </div>
                        <Grid container>
                            <Grid item xs>
                                <Link href="#" variant="body2">
                                    Forgot password?
                                </Link>
                            </Grid>
                            <Grid item>
                                <Link href="#" variant="body2">
                                    {"Don't have an account? Sign Up"}
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
                <Copyright sx={{ mt: 8, mb: 4 }} />
            </Container>

        </div>

    );
}