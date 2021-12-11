import React from "react";
import {
  EuiButton,
  EuiFieldText,
  EuiForm,
  EuiFormRow,
  EuiFieldPassword,
  EuiSpacer,
  EuiCheckbox,
  htmlIdGenerator,
} from "@elastic/eui";
import { Link } from "react-router-dom";
import validation from "../../utils/validation";
import styled from "styled-components";

const RegistrationFormWrapper = styled.div`
  padding: 2rem;
`;

const NeedAccountLink = styled.span`
  font-size: 0.8rem;
`;

const RegistrationForm = ({
  requestUserRegister = async ({ email, password, username }) =>
    console.log(`Logging in with  ${email} and ${username} and ${password}.`),
}) => {
  const [form, setForm] = React.useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });

  const [agreedToTerms, setAgreedToTerms] = React.useState(false);
  const [errors, setErrors] = React.useState({});

  const validateInput = (label, value) => {
    // grab validation function and run it on input if it exists
    // if it doesn't exists, just assume the input is valid
    const isValid = validation?.[label] ? validation?.[label]?.(value) : true;

    // set an error if the validation did not return true
    setErrors((errors) => ({ ...errors, [label]: !isValid }));
  };

  const setAgreedToTermsCheckbox = (e) => {
    setAgreedToTerms(e.target.checked);
  };

  const handleInputChange = (label, value) => {
    validateInput(label, value);
    setForm((form) => ({ ...form, [label]: value }));
  };

  const handlePasswordConfirmChange = (value) => {
    setErrors((errors) => ({
      ...errors,
      passwordConfirm:
        form.password !== value ? `Passwords do not match` : null,
    }));

    setForm((form) => ({ ...form, passwordConfirm: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // validate inputs before submitting
    Object.keys(form).forEach((label) => validateInput(label, form[label]));
    // if any input hasn't been entered in, return early
    if (!Object.values(form).every((value) => !!value)) {
      setErrors((errors) => ({
        ...errors,
        form: `You must fill out all fields`,
      }));
      return;
    }

    if (form.password !== form.passwordConfirm) {
      setErrors((errors) => ({
        ...errors,
        form: "Passwords do not  match",
      }));

      return;
    }

    if (!agreedToTerms) {
      setErrors((errors) => ({
        ...errors,
        form: "You must agree to the terms and conditions.",
      }));
      return;
    }

    await requestUserRegister({
      email: form.email,
      password: form.password,
      username: form.username,
    });
  };

  return (
    <RegistrationFormWrapper>
      <EuiForm
        component="form"
        onSubmit={handleSubmit}
        isInvalid={Boolean(errors.form)}
        error={[errors.form]}
      >
        <EuiFormRow
          label="Email"
          helpText="Enter the email associated with your account."
          isInvalid={Boolean(errors.email)}
          error={`Please enter a valid email.`}
        >
          <EuiFieldText
            icon="email"
            placeholder="user@gmail.com"
            value={form.email}
            onChange={(e) => handleInputChange("email", e.target.value)}
            aria-label="Enter the email associated with your account."
            isInvalid={Boolean(errors.email)}
          />
        </EuiFormRow>

        <EuiFormRow
          label="Username"
          helpText="Choose a username consisting solely of letters, numbers, underscores, and dashes."
          isInvalid={Boolean(errors.username)}
          error={`Username must be at least 3 characters.`}
        >
          <EuiFieldText
            icon="user"
            placeholder="phresh_2021"
            value={form.username}
            onChange={(e) => handleInputChange("username", e.target.value)}
            aria-label="Choose your original username."
            isInvalid={Boolean(errors.username)}
          />
        </EuiFormRow>

        <EuiFormRow
          label="Password"
          helpText="Enter your password."
          isInvalid={Boolean(errors.password)}
          error={`Password must be at least 7 characters`}
        >
          <EuiFieldPassword
            placeholder="••••••••••••"
            value={form.password}
            onChange={(e) => handleInputChange("password", e.target.value)}
            type="dual"
            aria-label="Enter your password."
            isInvalid={Boolean(errors.password)}
          />
        </EuiFormRow>

        <EuiFormRow
          label="Comfirm Password"
          helpText="Enter your password once again."
          isInvalid={Boolean(errors.passwordConfirm)}
          error={`Passwords must match.`}
        >
          <EuiFieldPassword
            placeholder="••••••••••••"
            value={form.passwordConfirm}
            onChange={(e) => handlePasswordConfirmChange(e.target.value)}
            type="dual"
            aria-label="Enter your password once again."
            isInvalid={Boolean(errors.passwordConfirm)}
          />
        </EuiFormRow>
        <EuiSpacer />
        <EuiCheckbox
          id={htmlIdGenerator()()}
          label="I agree to the terms and conditions."
          checked={agreedToTerms}
          onChange={(e) => setAgreedToTermsCheckbox(e)}
        />
        <EuiSpacer />

        <EuiButton type="submit" fill>
          Sign Up
        </EuiButton>
      </EuiForm>
      <EuiSpacer size="xl" />
      <NeedAccountLink>
        Already have an account? Log in <Link to="/login">here</Link>.
      </NeedAccountLink>
    </RegistrationFormWrapper>
  );
};

export default RegistrationForm;
