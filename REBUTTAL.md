## Reviewer_A_Q2

<b>GFI-signaling labels</b>: "good first issue","easy","Easy","low hanging fruit","minor bug","Easy Pick","Easy to Fix","good first bug","beginner","good first contribution","Good first task","newbie","starter bug","beginner-task","Minor Bug","easy-pick","minor feature","help wanted (easy)","up-for-grabs" and "good-first-bug" ([Tan et al.](https://doi.org/10.1145/3368089.3409746)).

## Reviewer_B_Q1/Reviewer_C_Q1

<table>
  <caption><b>Performance comparison with ICSME’18 for k = 0.</b></caption>
  <tr>
    <td></td>
    <td colspan="3" align="center">1st time point</td>
    <td colspan="3" align="center">2nd time point</td>
  </tr>
  <tr>
    <td>Approaches</td>
    <td align="center">AUC</td>
    <td align="center">Acc</td>
    <td align="center">R</td>
    <td align="center">AUC</td>
    <td align="center">Acc</td>
    <td align="center">R</td>
  </tr>
  <tr>
    <td>ICSME’18</td>
    <td>0.604</td>
    <td>0.808</td>
    <td>0.275</td>
    <td>0.604</td>
    <td>0.808</td>
    <td>0.275</td>
  </tr>
  <tr>
    <td>RecGFI</td>
    <td>0.792</td>
    <td>0.787</td>
    <td>0.623</td>
    <td>0.845</td>
    <td>0.832</td>
    <td>0.674</td>
  </tr>
</table>

## Reviewer_B_Q2

<table>
  <caption><b>Performance using 10-fold cross-validation by project (i.e., RecGFI is trained on issues from 90 projects and validated on issues from the other 10 projects).</b></caption>
  <tr>
    <td></td>
    <td colspan="3" align="center">1st time point</td>
    <td colspan="3" align="center">2nd time point</td>
  </tr>
  <tr>
    <td>k</td>
    <td align="center">AUC</td>
    <td align="center">Acc</td>
    <td align="center">R</td>
    <td align="center">AUC</td>
    <td align="center">Acc</td>
    <td align="center">R</td>
  </tr>
  <tr>
    <td>0</td>
    <td>0.687</td>
    <td>0.733</td>
    <td>0.485</td>
    <td>0.789</td>
    <td>0.796</td>
    <td>0.598</td>
  </tr>
  <tr>
    <td>1</td>
    <td>0.676</td>
    <td>0.711</td>
    <td>0.506</td>
    <td>0.780</td>
    <td>0.765</td>
    <td>0.627</td>
  </tr>
  <tr>
    <td>2</td>
    <td>0.689</td>
    <td>0.699</td>
    <td>0.569</td>
    <td>0.777</td>
    <td>0.756</td>
    <td>0.653</td>
  </tr>
  <tr>
    <td>3</td>
    <td>0.672</td>
    <td>0.676</td>
    <td>0.561</td>
    <td>0.782</td>
    <td>0.757</td>
    <td>0.660</td>
  </tr>
  <tr>
    <td>4</td>
    <td>0.687</td>
    <td>0.680</td>
    <td>0.565</td>
    <td>0.785</td>
    <td>0.754</td>
    <td>0.669</td>
  </tr>
</table>

## Reviewer_C_Q2

<table>
  <caption><b>AUC of baselines and RecGFI for k = 0 in four scenarios: a). cross-project, b). inside smaller dataset groups (ten projects in each group), c). inside one project, and d). trained on historical issues and validated on latest issues. (1st time point/2nd time point)</b></caption>
  <tr>
    <td></td>
    <td align="center">Logistic</td>
    <td align="center">Random Forest</td>
    <td align="center">MLP</td>
    <td align="center">ICSME’18</td>
    <td align="center">RecGFI</td>
  </tr>
  <tr>
    <td>Cross-Project</td>
    <td align="center">0.634/0.654</td>
    <td align="center">0.669/0.716</td>
    <td align="center">0.611/0.643</td>
    <td align="center">0.512/0.512</td>
    <td align="center">0.687/0.789</td>
  </tr>
  <tr>
    <td>Project Groups</td>
    <td align="center">0.736/0.766</td>
    <td align="center">0.760/0.796</td>
    <td align="center">0.745/0.753</td>
    <td align="center">0.651/0.651</td>
    <td align="center">0.782/0.836</td>
  </tr>
  <tr>
    <td>One Project</td>
    <td align="center">0.705/0.668</td>
    <td align="center">0.698/0.715</td>
    <td align="center">0.670/0.678</td>
    <td align="center">0.636/0.636</td>
    <td align="center">0.735/0.779</td>
  </tr>
  <tr>
    <td>Chronological</td>
    <td align="center">0.703/0.713</td>
    <td align="center">0.769/0.769</td>
    <td align="center">0.645/0.654</td>
    <td align="center">0.538/0.538</td>
    <td align="center">0.780/0.815</td>
  </tr>
</table>

Here are the detailed settings for each scenario:
* Cross-Project: We evaluate all models in the cross-project validation setting (i.e., trained on issues from 90 projects and validated on issues from the other 10 projects).
* Poject Groups: We divide the whole dataset into ten smaller sub-datasets (each sub-dataset contains issues from ten projects). We then train and evaluate all models in each of the smaller sub-datasets. For each sub-dataset, we use 10-fold cross-validation to obtain model performance and show the average performance across all sub-datasets in the table.
* One Project: We train and evaluate all models in even smaller sub-datasets (each sub-dataset contains issues from only one project).
* Chronological: We train and evaluate all models using the same setting as in Table 2 (i.e., trained with historical issues and validated on latest issues).
