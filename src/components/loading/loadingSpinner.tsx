import loading from "../../assets/loading.svg";
import "./loadingSpinner.scss";

export default function LoadingSpinner() {
  return (
    <>
      <li className="flex">
        <div> thinking</div>
        <img className="loadingSpinner" src={loading} />
      </li>
    </>
  );
}
