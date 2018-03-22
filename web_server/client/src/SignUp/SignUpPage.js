import React from 'react';
import SignUpForm from './SignUpForm';
import PropTypes from 'prop-types';

class SignUpPage extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            errors: {},
            user: {
                email: '',
                password: '',
                confirm_password: ''
            }
        }
    }

    processForm(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;
        const confirm_password = this.state.user.confirm_password;

        if (password !== confirm_password) {
            console.log('passwords not identical.');
            return;
        }

        console.log(email);
        console.log(password);

        const url = 'http://' + window.location.hostname + ':3000' + '/auth/signup';
        const request = new Request(
            url,
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json,',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );
        fetch(request)
            .then(response => {
                if (response.status === 200) {
                    this.setState({errors: {}});

                    response.json()
                        .then(json => {
                            console.log(json);

                            this.context.router.replace('/login');
                        });
                } else {
                    console.log('signup failed.');
                    response.json()
                        .then(json => {
                            const errors = json.errors ? json.errors : {};
                            errors.summary = json.message;
                            this.setState({errors: errors});
                        });
                }
            });
    }

    changeUser(event) {
        const field = event.target.name;
        const user = this.state.user;
        user[field] = event.target.value;

        this.setState({
            user: user
        });

        // passwaord and confirm_password should be identical
        if (this.state.user.password !== this.state.user.confirm_password) {
            const errors = this.state.errors;
            errors.password = 'Password and confirm password should be identical!';
            this.setState({errors: errors});
        } else {
            const errors = this.state.errors;
            errors.password = '';
            this.setState({errors: errors});
        }
    }

    render() {
        return (
            <SignUpForm
            onSubmit={(e) => this.processForm(e)}
            onChange={(e) => this.changeUser(e)}
            user={this.state.user}
            errors={this.state.errors}/>
        );
    }
}

SignUpPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default SignUpPage;