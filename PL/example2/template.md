###
IJ@
{
  "uuid": "{{uuid}}",
  "title": "{{title}}",
  "topic": "{{topic}}",
  "type": "v3" 
}
###
MC@
<pl-question-panel>
  <p>{{question}}</p>
</pl-question-panel>
<pl-multiple-choice answers-name="acc" weight="1">
  <pl-answer correct="{{flag1}}">{{option1}}</pl-answer>
  <pl-answer correct="{{flag2}}">{{option2}}</pl-answer>
  <pl-answer correct="{{flag3}}">{{option3}}</pl-answer>
  <pl-answer correct="{{flag4}}">{{option4}}</pl-answer>
</pl-multiple-choice>
###
CB@
<pl-question-panel>
<p>
  {{question}}
</p>
</pl-question-panel>
<pl-checkbox answers-name="select" hide-letter-keys="true" >
  <pl-answer correct="{{flag1}}">{{option1}}</pl-answer>
  <pl-answer correct="{{flag2}}">{{option2}}</pl-answer>
  <pl-answer correct="{{flag3}}">{{option3}}</pl-answer>
  <pl-answer correct="{{flag4}}">{{option4}}</pl-answer>
  <pl-answer correct="{{flag5}}">{{option5}}</pl-answer>
  
</pl-checkbox>
###
DD@
<pl-question-panel>
  <p>
    Select the correct option from the drop down list for each question bellow:
  </p>
</pl-question-panel>
<p>
  {{question1}}
  <pl-dropdown answers-name="HTML1">
    {% raw %}{{#params.HTML1}}{% endraw %}
        <pl-answer correct="{% raw %}{{tag}}{% endraw %}">{% raw %}{{ans}}{% endraw %}</pl-answer>
    {% raw %}{{/params.HTML1}}{% endraw %}
  </pl-dropdown> 
  {{question2}}
</p>

```
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "{{flag1}}", "ans": "{{option1}}"},
        {"tag": "{{flag2}}", "ans": "{{option2}}"},
        {"tag": "{{flag3}}", "ans": "{{option3}}"},
        {"tag": "{{flag4}}", "ans": "{{option4}}"}
    ]

    return data
```
###