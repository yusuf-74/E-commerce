import { Button } from '@mui/material'
import React, { useEffect } from 'react'
import apis from '../utils/axios/apis'

function Landing() {

  useEffect(() => {
    window.fbAsyncInit = function () {
      FB.init({
        appId: '319135230864852',
        cookie: true,
        xfbml: true,
        version: 'v18.0'
      });

      FB.AppEvents.logPageView();

    };

    (function (d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id))
        return;
      js = d.createElement(s);
      js.id = id;
      js.src = "https://connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
  },[])

  const sendAuthRequest = async () => {
    await apis.is_authenticated()
      .then(res => {
        if (res.status === 200) {
          window.alert("Authenticated")
        }
      })
      .catch(err => {
        window.alert("Not Authenticated")
      })
  }

  const getCalendarEvents = async () => {
    await apis.get_calendar_events()
      .then(res => {
        console.log(res.data)
      })
      .catch(err => {
        console.log(err)
      })
  }
  const handleFBAuth = async () => {
    /*global FB */
    FB.login(
      (response) => {
        console.log(response);
      },
      {
        config_id: '869616804765667',
        response_type: 'code',
        override_default_response_type: true
      }
    );
  }

  return (
    <>
      <div>Landing</div>
      <Button onClick={sendAuthRequest} variant="contained">make Authenticated request</Button>
      <br />
      <br />
      <Button onClick={getCalendarEvents} variant="contained">get calendar events</Button>
      <br />
      <br />

      <Button onClick={handleFBAuth}>
        LOGIN WITH FACEBOOK
      </Button>
    </>
  )
}

export default Landing