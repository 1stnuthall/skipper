// Contents of ./triggers/hello_world.ts
import { Trigger } from "deno-slack-sdk/types.ts";
import { TriggerContextData, TriggerTypes } from "deno-slack-api/mod.ts";
import HelloWorldWorkflow from "../workflows/hello_world.ts";

const trigger: Trigger<typeof HelloWorldWorkflow.definition> = {
  type: TriggerTypes.Shortcut,
  name: "Reverse a string",
  description: "Starts the workflow to reverse a string",
  workflow: `#/workflows/${HelloWorldWorkflow.definition.callback_id}`,
  inputs: {
    channel: {
      value: TriggerContextData.Shortcut.channel_id,
    },
  },
};

export default trigger;