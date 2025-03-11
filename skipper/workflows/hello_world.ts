// Contents of ./workflows/hello_world.ts
import { DefineWorkflow, Schema } from "deno-slack-sdk/mod.ts";
import { HelloWorldFunctionDef } from "../functions/hello_world.ts";

const HelloWorldWorkflowDef = DefineWorkflow({
  callback_id: "hello_world_workflow",
  title: "Hello World Workflow",
  input_parameters: {
    properties: {
      channel: {
        type: Schema.slack.types.channel_id,
      },
    },
    required: ["channel"],
  },
});

const helloWorldStep = HelloWorldWorkflowDef.addStep(HelloWorldFunctionDef, {});

HelloWorldWorkflowDef.addStep(Schema.slack.functions.SendMessage, {
  channel_id: HelloWorldWorkflowDef.inputs.channel,
  message: helloWorldStep.outputs.message,
});

export default HelloWorldWorkflowDef;