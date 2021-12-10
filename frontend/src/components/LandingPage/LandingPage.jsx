import React from "react";
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiFlexGroup,
  EuiFlexItem,
  EuiPageContentBody,
} from "@elastic/eui";
import styled from "styled-components";

// img
import heroGirl from "../../assets/img/HeroGirl.svg";
import dorm from "../../assets/img/Bed.svg";
import bedroom from "../../assets/img/Bedroom.svg";
import bathroom from "../../assets/img/Bathroom.svg";
import livingRoom from "../../assets/img/Living_room_interior.svg";
import kitchen from "../../assets/img/Kitchen.svg";
import readingRoom from "../../assets/img/Reading_room.svg";
import tvRoom from "../../assets/img/TV_room.svg";

// own components
import { Carousel, CarouselTitle } from "../../components";
import useCarousel from "../../hooks/useCarousel";

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
  padding-bottom: 5rem;
`;

const LandintTitle = styled.h1`
  font-size: 3.5rem;
  margin: 2rem 0;
`;

const StyledEuiPageContent = styled(EuiPageContent)`
  border-radius: 50%;
`;

const StyledEuiPageContentBody = styled(EuiPageContentBody)`
  max-width: 400px;
  max-height: 400px;
  & > img {
    width: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
`;

const carouselItems = [
  { label: "dorm room", content: <img src={dorm} alt="bed" /> },
  { label: "bedroom", content: <img src={bedroom} alt="bedroom" /> },
  { label: "bathroom", content: <img src={bathroom} alt="bathroom" /> },
  { label: "living room", content: <img src={livingRoom} alt="living room" /> },
  { label: "kitchen", content: <img src={kitchen} alt="kitchen" /> },
  {
    label: "reading room",
    content: <img src={readingRoom} alt="reading room" />,
  },
  { label: "tv room", content: <img src={tvRoom} alt="tv room" /> },
];

const LandingPage = (props) => {
  const { current } = useCarousel(carouselItems, 3000);
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <EuiFlexGroup direction="column" alignItems="center">
          <EuiFlexItem>
            <LandintTitle>Phresh Cleaners</LandintTitle>
          </EuiFlexItem>
          <EuiFlexItem>
            <CarouselTitle items={carouselItems} current={current} />
          </EuiFlexItem>
          <EuiFlexItem>
            <Carousel items={carouselItems} current={current} />
          </EuiFlexItem>

          <EuiFlexItem>
            <StyledEuiPageContent
              horizontalPosition="center"
              verticalPosition="center"
            >
              <StyledEuiPageContentBody>
                <img src={heroGirl} alt="girl" />
              </StyledEuiPageContentBody>
            </StyledEuiPageContent>
          </EuiFlexItem>
        </EuiFlexGroup>
      </EuiPageBody>
    </StyledEuiPage>
  );
};

export default LandingPage;
