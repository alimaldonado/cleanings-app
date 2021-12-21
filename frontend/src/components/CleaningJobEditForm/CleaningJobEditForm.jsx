import React, { useState } from "react";
import { connect } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Actions as cleaningActions } from "../../redux/cleanings";
import {
  EuiButton,
  EuiFieldText,
  EuiForm,
  EuiFormRow,
  EuiFieldNumber,
  EuiSuperSelect,
  EuiSpacer,
  EuiText,
  EuiTextArea,
} from "@elastic/eui";
import validation from "../../utils/validation";
import { extractErrorMessages } from "../../utils/errors";

const cleaningTypeOptions = [
  {
    value: "dust_up",
    inputDisplay: "Dust Up",
    dropdownDisplay: (
      <React.Fragment>
        <strong>Dust Up</strong>
        <EuiText size="s" color="subdued">
          <p className="euiTextColor--subdued">
            {`A minimal clean job. Dust shelves and mantels, tidy rooms, and sweep floors.`}
          </p>
        </EuiText>
      </React.Fragment>
    ),
  },
  {
    value: "spot_clean",
    inputDisplay: "Spot Clean",
    dropdownDisplay: (
      <React.Fragment>
        <strong>Spot Clean</strong>
        <EuiText size="s" color="subdued">
          <p className="euiTextColor--subdued">
            {`A standard clean job. Vacuum all indoor spaces, sanitize surfaces, and disinfect
              targeted areas. Bathrooms, tubs, and toilets can be added on for an additional charge.`}
          </p>
        </EuiText>
      </React.Fragment>
    ),
  },
  {
    value: "full_clean",
    inputDisplay: "Deep Clean",
    dropdownDisplay: (
      <React.Fragment>
        <strong>Deep Clean</strong>
        <EuiText size="s" color="subdued">
          <p className="euiTextColor--subdued">
            {`A complete clean job. Mop tile floors, scrub out tough spots, and a guaranteed clean
              residence upon completion. Dishes, pots, and pans included in this package.`}
          </p>
        </EuiText>
      </React.Fragment>
    ),
  },
];

const CleaningJobEditForm = ({
  cleaningJob,
  cleaningError,
  isUpdating,
  updateCleaning,
}) => {
  const { name, description, price, cleaning_type } = cleaningJob;
  const [form, setForm] = useState({
    name,
    description,
    price,
    cleaning_type,
  });

  const [errors, setErrors] = useState({});
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const navigate = useNavigate();
  const cleaningErrorList = extractErrorMessages(cleaningError);

  const validateInput = (label, value) => {
    // grab validation function and run it on input if it exists
    // if it doesn't exists, just assume the input is valid
    const isValid = validation?.[label] ? validation?.[label]?.(value) : true;
    setErrors((errors) => ({ ...errors, [label]: !isValid }));
  };

  const onInputChange = (label, value) => {
    validateInput(label, value);
    setForm((state) => ({ ...state, [label]: value }));
  };

  const onCleaningTypeChange = (cleaning_type) => {
    setForm((state) => ({ ...state, cleaning_type }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    Object.keys(form).forEach((label) => validateInput(label, form[label]));

    if (!Object.values(form).every((value) => Boolean(value))) {
      setErrors((errors) => ({
        ...errors,
        form: "You must fill out all fields.",
      }));
      return;
    }
    setHasSubmitted(true);

    const response = await updateCleaning({
      cleaning_id: cleaningJob.id,
      cleaning_update: { ...form },
    });

    if (response?.success) {
      const cleaningId = response.data?.id;

      navigate(`/cleaning-jobs/${cleaningId}`);
    }
  };
  const getFormErrors = () => {
    const formErrors = [];
    if (errors.form) {
      formErrors.push(errors.form);
    }
    if (hasSubmitted && cleaningErrorList.length) {
      return formErrors.concat(cleaningErrorList);
    }
    return formErrors;
  };

  return (
    <>
      <EuiForm
        component="form"
        onSubmit={handleSubmit}
        isInvalid={Boolean(getFormErrors().length)}
        error={getFormErrors}
      >
        <EuiFormRow
          label="Job Title"
          helpText="What do you want cleaners to see first?"
          isInvalid={Boolean(errors.name)}
          error={`Please enter a valid name.`}
        >
          <EuiFieldText
            name="name"
            value={form.name}
            onChange={(e) => onInputChange(e.target.name, e.target.value)}
          />
        </EuiFormRow>
        <EuiFormRow label="Select a cleaning type">
          <EuiSuperSelect
            options={cleaningTypeOptions}
            valueOfSelected={form.cleaning_type}
            onChange={(value) => onCleaningTypeChange(value)}
            itemLayoutAlign="top"
            hasDividers
          />
        </EuiFormRow>
        <EuiFormRow
          label="Hourly Rate"
          helpText="List a reasonable price for each hour of work the employee logs."
          isInvalid={Boolean(errors.price)}
          error={`Price should match the general format: 9.99`}
        >
          <EuiFieldNumber
            name="price"
            icon="currency"
            placeholder="19.99"
            value={form.price}
            onChange={(e) => onInputChange(e.target.name, e.target.value)}
          />
        </EuiFormRow>
        <EuiFormRow
          label="Job Description"
          helpText="What do you want prospective employees to know about this oportunity?"
          isInvalid={Boolean(errors.description)}
          error={`Please enter a valid input.`}
        >
          <EuiTextArea
            name="description"
            placeholder="I'm loking for..."
            value={form.description}
            onChange={(e) => onInputChange(e.target.name, e.target.value)}
          />
        </EuiFormRow>
        <EuiSpacer />
        <EuiButton
          type="submit"
          isLoading={isUpdating}
          fill
          iconType={"save"}
          iconSide="right"
        >
          Edit
        </EuiButton>
      </EuiForm>
    </>
  );
};

export default connect(
  (state) => ({
    cleaningError: state.cleanings.error,
    isUpdating: state.cleanings.isUpdating,
  }),
  {
    updateCleaning: cleaningActions.updateCleaningJob,
  }
)(CleaningJobEditForm);
