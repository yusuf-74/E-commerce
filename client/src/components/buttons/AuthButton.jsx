import React from 'react'
import Button from '@mui/material/Button';
import { Link } from 'react-router-dom';


function AuthButton({ label, link }) {
    return (
        <Link to={link}>
            <Button variant={label === 'Login' ? "contained":"outlined"} color="primary" sx={{margin:'0 8px'}}>
                {label}
            </Button>
        </Link>
    )
}

export default AuthButton