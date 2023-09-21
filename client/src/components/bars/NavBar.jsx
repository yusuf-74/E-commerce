import React from 'react'
import { Link } from "react-router-dom"
import styles from '../../styles/global/navbar.module.css'
import AuthButton from '../buttons/AuthButton'
import { Button } from '@mui/material'
function NavBar() {
    const NAV_ITEMS = [
        {
            label: 'Home',
            link: '/'
        },
        {
            label: 'About',
            link: 'about'
        },
        {
            label: 'Contact',
            link: 'contact'
        },
        {
            label: 'Register',
            link: 'auth/register'
        },
        {
            label: 'Login',
            link: 'auth/login'
        }
    ]
    const NAV_COMPONENTS = NAV_ITEMS.map(({ label, link }) => {
        if (label === 'Contact' /* pivote item */) {
            return (<li key={label} className={styles.pivotItem}>
                <Link to={link}>
                    <Button>
                        {label}
                    </Button>
                </Link>
            </li>)
        }
        else if (['Home','About'].includes(label) /* non-auth items */) {
            return (<li key={label}>
                <Link to={link}>
                    <Button>
                        {label}
                    </Button>
                </Link>
            </li>)
        }
        else {
            return (
                <li key = {label}>
                    <AuthButton label={label} link={link} />
                </li>
            
            )
        }

    })
    return (
        <ul className={styles.mainNavBar}>
            {NAV_COMPONENTS}
        </ul>
    )
}

export default NavBar