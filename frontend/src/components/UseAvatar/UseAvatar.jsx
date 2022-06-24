import { EuiAvatar } from "@elastic/eui";
import { getAvatarName } from "utils/format";

export default function UseAvatar({
  user,
  size = "l",
  initialsLength = 1,
  type = "user",
  color = null,
}) {
  return (
    <EuiAvatar
      size={size}
      name={getAvatarName(user)}
      imageUrl={user?.profile?.image}
      initialsLength={initialsLength}
      type={type}
      color={color}
    />
  );
}
