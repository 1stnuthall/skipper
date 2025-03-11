import { Manifest } from "deno-slack-sdk/mod.ts";
import HelloWorldWorkflow from "./workflows/hello_world.ts";

/**
 * The app manifest contains the app's configuration. This
 * file defines attributes like app name and description.
 * https://api.slack.com/automation/manifest
 */

export default Manifest({
  name: "skipper",
  description: "A Hello World app",
  icon: "assets/default_new_app_icon.png",
  workflows: [HelloWorldWorkflow],
  outgoingDomains: [],
  botScopes: ["chat:write", "chat:write.public"],
});