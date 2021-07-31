import React from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom';
import {AuthenticationProvider, oidcLog, withOidcSecure} from '@axa-fr/react-oidc-context';

import { Menu, Segment } from 'semantic-ui-react';


import oidcConfiguration from './configuration';

import Home from "./Home";
import About from "./About";
import Error from "./Error";
import UserInfo from "./UserInfo";

import './App.css';

function App() {
    let state = { activeItem: 'home' };

    return (
        <Router>
            <AuthenticationProvider configuration={oidcConfiguration} loggerLevel={oidcLog.DEBUG}>

                <div>
                    <Menu pointing secondary>
                        <Menu.Item name='home' as={Link} to='/'>Home</Menu.Item>
                        <Menu.Item name='about' as={Link} to='/about'>About</Menu.Item>
                        <Menu.Item name='secure' as={Link} to='/secure'>Secure</Menu.Item>
                        <Menu.Menu position='right'>
                            <Menu.Item name='logout' as={Link}>Logout</Menu.Item>
                        </Menu.Menu>
                    </Menu>
                </div>

                <Segment basic>
                    <Switch>
                        <Route exact path="/"><Home/></Route>
                        <Route path="/about"><About/></Route>
                        <Route path="/secure" component={withOidcSecure(UserInfo)}/>
                        <Route path="*"><Error/></Route>
                    </Switch>
                </Segment>
            </AuthenticationProvider>
        </Router>
    );
}


export default App;
