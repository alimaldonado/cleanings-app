import {
  EuiAvatar,
  EuiBadge,
  EuiButtonIcon,
  EuiFlexGroup,
  EuiFlexItem,
  EuiText,
} from "@elastic/eui";
import React from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
`;

const body = (
  <EuiText size="s">
    <p>
      Lorem ipsum dolor sit amet consectetur, adipisicing elit. Non officiis
      porro esse eaque iste officia mollitia error magnam ipsam ipsum!
    </p>
  </EuiText>
);

const copyAction = (
  <EuiButtonIcon
    title="Custom Action"
    aria-label="Custom Action"
    color="subdued"
    iconType="copy"
  />
);

const complexEvent = (
  <EuiFlexGroup responsive={false} alignItems="center" gutterSize="s">
    <EuiFlexItem grow={false}>added tags</EuiFlexItem>
    <EuiFlexItem grow={false}>
      <EuiBadge color="primary">sample</EuiBadge>
    </EuiFlexItem>
    <EuiFlexItem grow={false}>
      <EuiBadge color="secondary">review</EuiBadge>
    </EuiFlexItem>
  </EuiFlexGroup>
);

const complexUsername = (
  <EuiFlexGroup responsive={false} alignItems="center" gutterSize="s">
    <EuiFlexItem grow={false}>
      <EuiAvatar size="s" type="space" name="Pedro" />
    </EuiFlexItem>
    <EuiFlexItem grow={false}>pedror</EuiFlexItem>
  </EuiFlexGroup>
);

const longBody = (
  <EuiText size="s">
    <p>
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Iure qui
      consequuntur cumque nihil soluta dolorem quas sint temporibus, ab debitis
      veritatis, ad nulla! Inventore quasi minima nam? Cum voluptatum provident
      aspernatur, sed suscipit consequatur ab quaerat dolores, natus doloribus
      amet impedit dolorem assumenda praesentium consectetur? Odio earum
      eligendi laborum id.
    </p>
  </EuiText>
);

const avatar = (
  <EuiAvatar
    imageUrl="https://source.unsplash.com/64x64/?woman"
    size="l"
    name="Juana"
  />
);

const comments = [
  {
    username: "janed",
    event: "added a comment",
    timestamp: "on Jan 1, 2020",
    children: body,
    actions: copyAction,
  },
  {
    username: "juanab",
    type: "update",
    actions: copyAction,
    event: "pushed incident X0Z235",
    timestamp: "on Jan 3, 2020",
    timelineIcon: avatar,
  },
  {
    username: "pancho1",
    type: "update",
    event: "edited case",
    timestamp: "on Jan 9, 2020",
  },
  {
    username: complexUsername,
    type: "update",
    actions: copyAction,
    event: complexEvent,
    timestamp: "on Jan 11, 2020",
    timelineIcon: "tag",
  },
  {
    username: "elohar",
    event: "added a comment",
    timestamp: "on Jan 14, 2020",
    timelineIcon: <EuiAvatar size="l" name="Eloha" />,
    children: longBody,
    actions: copyAction,
  },
];

const CleaningActivityFeed = () => {
  return (
    <Wrapper>
      <EuiCommentList comments={comments} />
    </Wrapper>
  );
};

export default CleaningActivityFeed;
