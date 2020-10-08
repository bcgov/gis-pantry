# HTML Popup Modification

Use HTML to modify characteristics of the popup in your application

## Use Case

Using HTML allows the user to have greater control in how the popup behaves and looks. Provides much greater functionality than the default popup function.


## Workflow

In this example use the created HTML and place it in configure a customized attribute display for the layer in Arc GIS online


## Expression Template

```
<br /><br />
<div style="padding:10px;background-color:rgb(3,223,252)"><b>Visual Quality Hazard</b></div>
<table style="width:100%;">
  <tbody>
<tr>
    <td style="border:0.5px solid rgb(215,215,215)"><b>Green up Area</b></td>
    <td style="border:0.5px solid rgb(215,215,215)">{GREENUP_AREA}<br /></td> 
  </tr>
<tr>
    <td style="border:0.5px solid rgb(215,215,215)"><b>Contributing Area</b>
	</td><td style="border:0.5px solid rgb(215,215,215)">{CONTRIBUTING_AREA}</td> 
  </tr>
<tr>
    <td style="border:0.5px solid rgb(215,215,215)"><b>Upper VLI Target Percent</b></td>
	<td style="border:0.5px solid rgb(215,215,215)">{VLI_TARGETS_UPPER_PERCENT} </td> 
  </tr>
<tr>
    <td style="border:0.5px solid rgb(215,215,215)"><b>Green Up Percent</b></td>
	<td style="border:0.5px solid rgb(215,215,215)">{GREENUP_PERCENT} </td> 
  </tr>
<tr>
    <td style="border:0.5px solid rgb(215,215,215)"><b>Non Green up Percent</b></td>
	<td style="border:0.5px solid rgb(215,215,215)">{NON_GREEN_UP_PERCENT}</td> 
  </tr>
<tr>
    <td style="border:0.5px solid rgb(215,215,215)"><b>Visual objective risk</b></td>
	<td style="border:0.5px solid rgb(215,215,215)">{VLI_RISK}</td> 
  </tr>
</tbody></table>
```

## Example Output
![HTML_Image](..\Images\HTML_Popup_Customization.gif)



### License
    Copyright 2019 BC Provincial Government

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
