{
  Output a list of models in a cell to a csv including their mesh, location, rotation, and scale.
}
unit UserScript;

const
  sRefSignatures = 'REFR,ACHR,PGRE,PMIS,PHZD,PARW,PBAR,PBEA,PCON,PFLA';
var
  slModels: TStringList;
var cellName: string;
function Initialize: integer;
begin
  // list of models, ignore duplicated ones
  slModels := TStringList.Create;
  slModels.Sorted := True;
  slModels.Duplicates := dupIgnore;
end;

function Process(e: IInterface): integer;
var
  s: string;
  r: IInterface;
begin
  cellName := EditorID(e);
  if Pos(Signature(e), sRefSignatures) = 0 then
    Exit;
    
  
  r := BaseRecord(e);
  
  if not Assigned(r) then
    Exit;

  r := WinningOverride(r);

  if Signature(r) = 'ARMO' then
    s := GetElementEditValues(r, 'Male world model\MOD2')
  else
    s := GetElementEditValues(r, 'Model\MODL');

  if s <> '' then
    s := s + ',' + GetElementEditValues(e, 'DATA\Position\X') + ',' + GetElementEditValues(e, 'DATA\Position\Y') + ',' + GetElementEditValues(e, 'DATA\Position\Z') + ',' + GetElementEditValues(e, 'DATA\Rotation\X') + ',' + GetElementEditValues(e, 'DATA\Rotation\Y') + ',' + GetElementEditValues(e, 'DATA\Rotation\Z') + ',' + GetElementEditValues(e, 'XSCL');
    slModels.Add(LowerCase(s));
end;

function Finalize: integer;
begin
  AddMessage('Finished Executing');
  slModels.SaveToFile(cellName+'.txt');
  slModels.Free;
end;

end.
